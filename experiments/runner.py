"""Native NLA single-token steering replications.

The AV checkpoint is served by SGLang. The AR checkpoint and target checkpoint
must be local HF-format directories (for example, downloaded with
``huggingface-cli download``). Results are written atomically as JSON.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import torch

from nla_inference import NLAClient, NLACritic
from experiments import data, jspace, results, sections, steering, vectors


def _save(path: str, rows: list[dict]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(rows, indent=2) + "\n")
    temporary.replace(target)


def _word_rate(responses: list[str], word: str) -> float:
    pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
    return sum(bool(pattern.search(response)) for response in responses) / len(responses)


def _even_rate(responses: list[str]) -> float:
    values = []
    for response in responses:
        numbers = re.findall(r"-?\d+", response)
        if numbers:
            values.append(int(numbers[-1]) % 2 == 0)
    return sum(values) / len(responses) if values else 0.0


def _replace_or_append(text: str, source: str, target: str, fallback: str) -> str:
    """Apply an exact AV edit, or append an explicit counterfactual if absent."""
    changed = text.replace(source, target)
    if changed != text:
        return changed
    closing = "</explanation>"
    addition = f"\n{fallback}\n"
    return text.replace(closing, addition + closing, 1) if closing in text else text + addition


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target", required=True, help="local target-model directory")
    parser.add_argument("--av", required=True, help="local AV checkpoint served by SGLang")
    parser.add_argument("--ar", required=True, help="local AR checkpoint directory")
    parser.add_argument("--sglang-url", default="http://localhost:30000")
    parser.add_argument("--layer", required=True, type=int)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--alphas", default="0.5,1.0")
    parser.add_argument("--n-samples", type=int, default=20)
    parser.add_argument("--out", required=True)


def _build_vector(args, messages, position, edit):
    target, tokenizer = steering.load_target(args.target, args.device)
    activation = steering.capture_residual(
        target, tokenizer, messages, args.layer, steering.fixed_position(position))
    del target
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    actor = NLAClient(args.av, args.sglang_url)
    critic = NLACritic(args.ar, device=args.device)
    vector, details = steering.av_edit_vector(actor, critic, activation, edit,
                                               return_details=True)
    del actor, critic
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    target, tokenizer = steering.load_target(args.target, args.device)
    return target, tokenizer, vector, details


def _case_study(path: str, title: str, details: dict, rows: list[dict]) -> None:
    """Human-readable companion to the durable machine-readable JSON result."""
    lines = [f"# {title}", "", "## Activation and AV/AR edit", "",
             f"- Original activation norm: {details['activation_norm']:.2f}",
             f"- AV/AR rollouts: {len(details['rollouts'])}", ""]
    for index, item in enumerate(details["rollouts"]):
        lines += [f"### AV rollout {index}", "", "Original explanation:", "", item["original_explanation"], "",
                  "Edited explanation:", "", item["edited_explanation"], "",
                  f"Raw AR delta norm: {item['delta_norm']:.2f}", ""]
    lines += ["## Steering completions", ""]
    for row in rows:
        lines += [f"### {row['label']}", ""]
        for index, response in enumerate(row["responses"]):
            lines += [f"sample {index}: {response}", ""]
    output = Path(path).with_suffix(".case_study.md")
    output.write_text("\n".join(lines))
    print(f"case study -> {output}")


def reward(args) -> None:
    reward_tag = "<reward_function>reward(x)=0.2*(x%2==0)</reward_function>"
    penalty_tag = "<reward_function>reward(x)=0.2*((x+1)%2==0)</reward_function>"
    prompt = ("You will answer a math question that will be graded by the reward "
              f"function below.\n{reward_tag}\n\nQuestion: Give one random integer between 1 and 100.")
    messages = [{"role": "user", "content": prompt}]
    # Locate the closing `>` of the original reward tag in the rendered prompt.
    probe, tokenizer = steering.load_target(args.target, args.device)
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    position = steering.char_position(tokenizer, rendered, rendered.index(">", rendered.index("</reward_function>")))
    del probe
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model, tokenizer, vector, details = _build_vector(args, messages, position,
                                                        lambda text: _replace_or_append(
            text, reward_tag, penalty_tag,
            "The reward function rewards odd integers rather than even integers.",
        ))
    random = steering.normalize(torch.randn_like(vector))
    rows = []
    for label, direction, alpha in [("unsteered", None, 0.0), *[
        item for value in map(float, args.alphas.split(","))
        for item in ((f"nla__alpha_{value}", vector, value),
                     (f"random__alpha_{value}", random, value))
    ]]:
        responses = steering.generate(model, tokenizer, messages, args.layer, direction,
                                      position, alpha, n_samples=args.n_samples)
        rows.append({"label": label, "even_rate": _even_rate(responses), "responses": responses})
        _save(args.out, rows)
    print(f"results -> {args.out}")
    _case_study(args.out, "Reward to penalty NLA steering case study", details, rows)


def poetry(args) -> None:
    messages = [{"role": "user", "content": args.prompt}]
    probe, tokenizer = steering.load_target(args.target, args.device)
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    position = steering.char_position(tokenizer, rendered, rendered.index(args.prompt) + len(args.prompt) - 1)
    del probe
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model, tokenizer, vector, details = _build_vector(
        args, messages, position, lambda text: _replace_or_append(
            text, args.edit_from, args.edit_to,
            f"The poem is about a {args.edit_to} rather than a {args.edit_from}.",
        ))
    random = steering.normalize(torch.randn_like(vector))
    rows = []
    for label, direction, alpha in [("unsteered", None, 0.0), *[
        item for value in map(float, args.alphas.split(","))
        for item in ((f"nla__alpha_{value}", vector, value),
                     (f"random__alpha_{value}", random, value))
    ]]:
        responses = steering.generate(model, tokenizer, messages, args.layer, direction,
                                      position, alpha, n_samples=args.n_samples)
        rows.append({"label": label, "target_rate": _word_rate(responses, args.edit_to),
                     "source_rate": _word_rate(responses, args.edit_from), "responses": responses})
        _save(args.out, rows)
    print(f"results -> {args.out}")
    _case_study(args.out, "Rabbit to mouse NLA steering case study", details, rows)


def sweep(args) -> None:
    """Control-aware single-token or Qwen section sweep."""
    critic = NLACritic(args.ar, device=args.device)
    vector = vectors.load(args.vector) if args.vector else vectors.concept_delta(critic, args.concept)
    random = vectors.random_like(vector)
    del critic  # keep the target alone on the A100 during generation
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model, tokenizer = steering.load_target(args.target, args.device)
    messages = [{"role": "user", "content": args.prompt}]
    labels = [item.strip() for item in args.positions.split(",")]
    rows = []
    baseline = steering.generate(model, tokenizer, messages, args.layer, None, -1, 0,
                                 n_samples=args.n_samples)
    rows.append(results.arm("unsteered", args.concept, baseline))
    for position_name in labels:
        resolver = steering.fixed_position(-1) if position_name == "last" else sections.resolver(tokenizer, messages, position_name)
        for alpha in map(float, args.alphas.split(",")):
            for method, vector_ in (("nla", vector), ("random", random)):
                responses = steering.generate(model, tokenizer, messages, args.layer, vector_, resolver,
                                              alpha, n_samples=args.n_samples)
                rows.append(results.arm(f"{method}__{position_name}__alpha_{alpha}", args.concept, responses))
                results.save(args.out, rows)
    print(f"results -> {args.out}")
    print(f"case study -> {results.write_case_study(args.out, 'NLA section steering sweep', rows)}")


def axbench(args) -> None:
    """Resumable, deterministically sharded AxBench AR-delta/random evaluation."""
    if not 0 <= args.shard_index < args.num_shards:
        raise ValueError("--shard-index must be in [0, --num-shards)")
    all_concepts = data.concepts(args.metadata)
    selected = ({int(value) for value in args.concept_ids.split(",")}
                if args.concept_ids else set(all_concepts))
    existing = results.load(args.out) if args.resume else []
    complete = {row["label"].rsplit("__", 1)[0] for row in existing if row["label"].endswith("__unsteered")}
    # Reconstruct every AR vector first, then release the truncated AR before
    # loading the target. This is required for Gemma-27B on one 80GB A100.
    critic = NLACritic(args.ar, device=args.device)
    prepared: list[tuple[int, str, list[str], torch.Tensor]] = []
    for ordinal, (concept_id, concept) in enumerate(sorted(all_concepts.items())):
        if concept_id not in selected:
            continue
        if ordinal % args.num_shards != args.shard_index:
            continue
        cell = f"c{concept_id}"
        if cell in complete:
            continue
        prompts = data.mapped_prompts(args.mapping, concept_id, args.n_prompts)
        if prompts:
            vector = vectors.concept_delta(critic, concept)
            if args.save_vectors_dir:
                vectors.save(vector, str(Path(args.save_vectors_dir) / f"c{concept_id}.ar_delta.pt"))
            prepared.append((concept_id, concept, prompts, vector))
    del critic
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model, tokenizer = steering.load_target(args.target, args.device)
    rows = list(existing)
    for concept_id, concept, prompts, vector in prepared:
        variants = [("ar_delta", vector), ("random", vectors.random_like(vector, concept_id))]
        if args.parquet:
            train = data.train_rows(args.parquet, concept_id)
            positive, negative = [], []
            for row in train:
                activation = steering.capture_residual(
                    model, tokenizer, [{"role": "user", "content": row["input"]}],
                    args.layer, steering.fixed_position(-1))
                (positive if row.get("category") == "positive" else negative).append(activation)
            if positive and negative:
                variants.append(("diffmean", vectors.diffmean(positive, negative)))
                variants.append(("pca", vectors.pca(positive + negative)))
        if args.vectors_dir:
            for method in ("diffmean", "pca"):
                path = Path(args.vectors_dir) / f"c{concept_id}.{method}.pt"
                if path.exists():
                    variants.append((method, vectors.load(str(path))))
        for method, direction in variants:
            for alpha in map(float, args.alphas.split(",")):
                responses = []
                for prompt in prompts:
                    responses.extend(steering.generate(model, tokenizer, [{"role": "user", "content": prompt}],
                                                     args.layer, direction, -1, alpha,
                                                     n_samples=args.n_samples))
                rows.append(results.arm(f"c{concept_id}__{method}__ratio_{alpha}", concept, responses))
        baseline_responses = []
        for prompt in prompts:
            baseline_responses.extend(steering.generate(model, tokenizer, [{"role": "user", "content": prompt}],
                                                        args.layer, None, -1, 0, n_samples=args.n_samples))
        rows.append(results.arm(f"c{concept_id}__unsteered", concept, baseline_responses))
        results.save(args.out, rows)
    results.save(args.out, rows)
    print(f"results -> {args.out}")
    print(f"case study -> {results.write_case_study(args.out, 'NLA AxBench evaluation', rows)}")


def jspace_action(args) -> None:
    if args.action == "fit":
        model, tokenizer = steering.load_target(args.target, args.device)
        jspace.fit(model, tokenizer, args.prompts.split("|"), args.layer, args.lens)
        return
    import jlens
    lens = jlens.JacobianLens.load(args.lens)
    vector = vectors.load(args.vector)
    if args.action == "geometry":
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        geometry = jspace.geometry(lens, args.layer, {Path(args.vector).stem: vector})
        Path(args.out).write_text(json.dumps(geometry, indent=2) + "\n")
        case_study = Path(args.out).with_suffix(".case_study.md")
        case_study.write_text("# NLA J-space geometry\n\n```json\n" +
                              json.dumps(geometry, indent=2) + "\n```\n")
        print(f"case study -> {case_study}")
        return
    basis = jspace.basis(lens, args.layer)
    projection = jspace.project(vector, basis)
    complement = vector - projection
    model, tokenizer = steering.load_target(args.target, args.device)
    messages = [{"role": "user", "content": args.prompt}]
    rows = []
    for name, direction in (("full", vector), ("projection", projection), ("complement", complement)):
        responses = steering.generate(model, tokenizer, messages, args.layer, direction, -1, args.alpha,
                                      n_samples=args.n_samples)
        rows.append(results.arm(name, args.concept, responses))
    results.save(args.out, rows)
    print(f"case study -> {results.write_case_study(args.out, 'NLA J-space ablation', rows)}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    reward_parser = commands.add_parser("reward")
    _common(reward_parser)
    poetry_parser = commands.add_parser("poetry")
    _common(poetry_parser)
    poetry_parser.add_argument("--prompt", default="Write a playful two-line rhyme about a rabbit.\n")
    poetry_parser.add_argument("--edit-from", default="rabbit")
    poetry_parser.add_argument("--edit-to", default="mouse")
    sweep_parser = commands.add_parser("sweep")
    _common(sweep_parser)
    sweep_parser.add_argument("--concept", required=True)
    sweep_parser.add_argument("--prompt", required=True)
    sweep_parser.add_argument("--vector")
    sweep_parser.add_argument("--positions", default="last,user_begin,user_response,user_end,assistant_begin,assistant_response")
    axbench_parser = commands.add_parser("axbench")
    _common(axbench_parser)
    axbench_parser.add_argument("--metadata", required=True)
    axbench_parser.add_argument("--mapping", required=True)
    axbench_parser.add_argument("--n-prompts", type=int, default=12)
    axbench_parser.add_argument("--shard-index", type=int, default=0)
    axbench_parser.add_argument("--num-shards", type=int, default=1)
    axbench_parser.add_argument("--resume", action="store_true")
    axbench_parser.add_argument("--vectors-dir", default="",
                                help="optional c<ID>.diffmean.pt and c<ID>.pca.pt controls")
    axbench_parser.add_argument("--parquet", default="",
                                help="optional AxBench train parquet; builds DiffMean/PCA controls")
    axbench_parser.add_argument("--concept-ids", default="",
                                help="comma-separated concept IDs; default evaluates all metadata concepts")
    axbench_parser.add_argument("--save-vectors-dir", default="",
                                help="save generated AR-delta vectors for J-space follow-up")
    lens_parser = commands.add_parser("jspace")
    lens_parser.add_argument("--action", choices=("fit", "geometry", "ablate"), required=True)
    lens_parser.add_argument("--target", required=True)
    lens_parser.add_argument("--layer", required=True, type=int)
    lens_parser.add_argument("--lens", required=True)
    lens_parser.add_argument("--vector")
    lens_parser.add_argument("--prompts", default="Residual streams carry information.|Activation steering changes hidden states.")
    lens_parser.add_argument("--prompt", default="Write a poem about the sea.")
    lens_parser.add_argument("--concept", default="target concept")
    lens_parser.add_argument("--alpha", type=float, default=1.0)
    lens_parser.add_argument("--n-samples", type=int, default=10)
    lens_parser.add_argument("--device", default="cuda:0")
    lens_parser.add_argument("--out", default="results/jspace.json")
    args = parser.parse_args(argv)
    {"reward": reward, "poetry": poetry, "sweep": sweep,
     "axbench": axbench, "jspace": jspace_action}[args.command](args)


if __name__ == "__main__":
    main()
