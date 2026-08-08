# Qwen/Gemma NLA A100 reproduction, recovery, and findings guide

This is the single entry point for restoring, running, inspecting, and
interpreting the Qwen2.5-7B and Gemma 3 12B natural-language-autoencoder (NLA)
steering experiments in this repository. It also records what must survive the
original Vast A100 instance.

## 1. Backup status before releasing the original A100

The generated data is backed up in GitHub, while public/gated Hugging Face
downloads are intentionally excluded.

- GitHub fork: `https://github.com/gmath-cdr/natural_language_autoencoders.git`
- Data commit verified on `origin/main`: `8c65e2bee9bf411679d7c9858dacfc95b67b70dc`
- Exact hash audit: `artifacts/cross_model_extended_2026-08-08/protocol/backup_audit.json`
- New-bundle checksums: `artifacts/cross_model_extended_2026-08-08/SHA256SUMS`
- Worktree was clean and local/remote `main` matched when the audit was made.

The audit compared `/workspace/nla/results`, `/workspace/nla/vectors`, and
`/workspace/nla/checkpoints` against tracked files:

| Generated type | Local files | Exact SHA-256 matches in `artifacts/` |
|---|---:|---:|
| Result JSON | 46 | 46 |
| Prompt mapping JSONL | 5 | 5 |
| Vectors, fitted lenses, and fit checkpoints (`*.pt*`) | 30 | 30 |
| Derived `*.case_study.md` | 34 | 34 tracked name matches |

Trailing whitespace was normalized in some archived Markdown case studies.
Their canonical JSON sources are exact hash matches. No generated model result,
saved vector, fitted lens, or resumable lens checkpoint depends on retaining the
original A100 filesystem.

Not stored in GitHub because they are recoverable downloads:

| Role | Qwen profile | Gemma profile |
|---|---|---|
| Target | `Qwen/Qwen2.5-7B-Instruct` | `google/gemma-3-12b-it` |
| AR | `kitft/nla-qwen2.5-7b-L20-ar` | `kitft/nla-gemma3-12b-L32-ar` |
| AV | `kitft/nla-qwen2.5-7b-L20-av` | `kitft/nla-gemma3-12b-L32-av` |
| Intervention layer | 20 | 32 |

The Gemma target is gated. Accept its Hugging Face license before restoring.
Do not substitute checkpoint IDs or layers.

## 2. File map

Read these in order:

1. This guide: setup, execution sequence, exact commands, recovery, and summary.
2. `scripts/vast_setup.sh`: executable one-A100 bootstrap and SGLang lifecycle.
3. `experiments/README.md`: package architecture and general command reference.
4. `QWEN_7B_STEERING_FINDINGS.md`: complete Qwen experiment narrative.
5. `GEMMA_12B_STEERING_FINDINGS.md`: complete Gemma experiment narrative.
6. `artifacts/cross_model_extended_2026-08-08/README.md`: extended cross-model
   findings, tables, cautions, and artifact layout.
7. `artifacts/cross_model_extended_2026-08-08/summary_metrics.json`: compact
   machine-readable final metrics.
8. `artifacts/cross_model_extended_2026-08-08/protocol/run_protocol.json`: exact
   alphas, samples, positions, seeds, and prompt counts.

Artifact bundles:

| Path | Contents |
|---|---|
| `artifacts/qwen2.5-7b/full_run/` | All initial Qwen reward, poetry, nautical, concept-3, tiny-lens results, vector, lens, and fit checkpoints |
| `artifacts/qwen2.5-7b/axbench_c3_spot/` | Curated first concept-3/J-space spot check |
| `artifacts/qwen2.5-7b/axbench_c3_broad12/` | Qwen 12-prompt concept-3 run, broad lens, prompts, vector, geometry, and original normalized-component ablation |
| `artifacts/qwen2.5-7b/axbench_diverse6/` | Qwen 6,840-generation six-concept expansion and six vectors |
| `artifacts/gemma3-12b/full_run/` | Gemma smoke, reward, poetry, nautical, concept-3, broad lens/vector, fit checkpoints, and ablations |
| `artifacts/cross_model_extended_2026-08-08/` | Gemma six-concept expansion; corrected Qwen ablation; both-model readouts, reframing, geometry correlations, turn sweeps, vectors, metrics, protocols, and audit |

Every bundle containing `SHA256SUMS` can be checked independently.

## 3. Restore a fresh Vast instance

Use one idle 80 GB A100. A persistent volume with at least 260 GB free is a
comfortable target if both profiles will be downloaded together.

```bash
cd /workspace
mkdir -p steering
cd steering
git clone https://github.com/gmath-cdr/natural_language_autoencoders.git
cd natural_language_autoencoders

python -m pip install --upgrade pip
hf auth login
```

The setup script installs this repository, SGLang, and download dependencies;
downloads the exact target/AR/AV profile; preserves the pre-existing Hugging
Face token location when redirecting caches; starts AV SGLang with
`--mem-fraction-static 0.35`; and runs preflight.

### Qwen setup

```bash
bash scripts/vast_setup.sh --profile qwen2.5-7b --workspace /workspace/nla
source /workspace/nla/qwen2.5-7b.env
```

### Switch to Gemma

Only one AV server may own port 30000. Stop Qwen, then start Gemma:

```bash
bash scripts/vast_setup.sh --profile qwen2.5-7b \
  --workspace /workspace/nla --stop-server
bash scripts/vast_setup.sh --profile gemma3-12b --workspace /workspace/nla
source /workspace/nla/gemma3-12b.env
```

Gemma setup disables only SGLang's incompatible CUDA-graph prefill backend;
decode graphs remain enabled. If models are already present, add
`--skip-download`. To use only AR/target experiments without AV decoding, add
`--skip-server`.

### Optional Jacobian-lens installation

The run used this exact fork/revision:

```text
https://github.com/gmath-cdr/jacobian-lens.git
581d398613e5602a5af361e1c34d3a92ea82ba8e
```

Restore it with:

```bash
cd /workspace/steering
git clone https://github.com/gmath-cdr/jacobian-lens.git
git -C jacobian-lens checkout 581d398613e5602a5af361e1c34d3a92ea82ba8e
python -m pip install -e /workspace/steering/jacobian-lens
export PYTHONPATH=/workspace/steering/jacobian-lens
cd /workspace/steering/natural_language_autoencoders
```

The AxBench checkout used revision
`41c8332543e5a631f9a8c0a9df38799893ace758` from
`https://github.com/gmath-cdr/axbench.git`. It is not required to replay these
seven concepts: the exact metadata rows and held-out mappings are committed in
this repository.

## 4. Validate restoration before using the GPU

```bash
python -m py_compile experiments/*.py

for bundle in \
  artifacts/qwen2.5-7b/full_run \
  artifacts/qwen2.5-7b/axbench_c3_spot \
  artifacts/qwen2.5-7b/axbench_c3_broad12 \
  artifacts/qwen2.5-7b/axbench_diverse6 \
  artifacts/gemma3-12b/full_run \
  artifacts/cross_model_extended_2026-08-08
do
  if [ -f "$bundle/SHA256SUMS" ]; then
    (cd "$bundle" && sha256sum -c SHA256SUMS)
  fi
done
```

With a profile loaded and its AV server running:

```bash
python -m experiments.preflight \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" \
  --sglang-url http://127.0.0.1:30000 --require-cuda
```

Preflight requires `nla_meta.yaml` only for AR and AV checkpoints, not for the
base target model.

## 5. Recommended execution order

Do not begin Gemma, full AxBench, or a large J-space study until Qwen works.

1. Qwen technical reward smoke.
2. Qwen reward and poetry proofpoints; inspect both case studies.
3. Qwen concept-3 casino AxBench run with unsteered/random controls.
4. Qwen six-concept expansion.
5. Qwen broad-12 lens, corrected ablation, token readout, and geometry.
6. Qwen reframing and turn-position checks.
7. Stop Qwen AV; set up Gemma.
8. Gemma reward/poetry/nautical spot checks.
9. Gemma concept-3 low-alpha calibration.
10. Gemma six-concept expansion.
11. Gemma broad-lens readout/geometry, reframing, and turn-position checks.
12. Inspect `*.case_study.md`, generate/check metrics, checksum, commit, push.

Results are stochastic because sampling seeds for text generation are not
fixed. Random-control seeds fix the random directions, not every sampled token.
Expect statistical agreement rather than byte-identical generations.

## 6. Qwen smoke and paper-style proofpoints

```bash
source /workspace/nla/qwen2.5-7b.env

# Technical smoke: one sample and one alpha.
python -m experiments.runner reward \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" --layer 20 \
  --anchor condition --alphas 0.5 --n-samples 1 --random-seeds 42 \
  --out "$NLA_RESULTS/reward_smoke.json"

# Credible reward control set.
python -m experiments.runner reward \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" --layer 20 \
  --anchor condition --alphas 0.5,1.0 --n-samples 20 \
  --random-seeds 17,42,101 \
  --out "$NLA_RESULTS/reward_grounded.json"

# Rabbit-to-mouse poetry analogue.
python -m experiments.runner poetry \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" --layer 20 \
  --alphas 0.5,0.75,1.0 --n-samples 20 --random-seeds 17,42,101 \
  --out "$NLA_RESULTS/poetry.json"
```

Inspect the generated `reward_grounded.case_study.md` and
`poetry.case_study.md`. The public Qwen model cannot recreate Anthropic's
private Claude activation, so poetry is a procedural analogue, not an exact
model replication.

## 7. AxBench concept runs

The exact metadata is committed at
`experiments/configs/axbench_concepts_9b_l20.jsonl`. Exact held-out prompt
mappings are stored in the artifact bundles. `--resume` skips concepts whose
unsteered arm is already atomically complete.

### Qwen concept 3

```bash
source /workspace/nla/qwen2.5-7b.env

python -m experiments.runner axbench \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" --layer 20 \
  --metadata experiments/configs/axbench_concepts_9b_l20.jsonl \
  --mapping artifacts/qwen2.5-7b/axbench_c3_broad12/results/axbench_c3_broad_mapping.jsonl \
  --concept-ids 3 --n-prompts 12 --n-samples 5 \
  --alphas 0.5,0.75,1.0 --random-seeds 17,42,101,314,2718 \
  --save-vectors-dir "$NLA_VECTORS/axbench_c3_broad" --resume \
  --out "$NLA_RESULTS/axbench_c3_broad.json"
```

### Qwen six-concept expansion

```bash
python -m experiments.runner axbench \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" --layer 20 \
  --metadata experiments/configs/axbench_concepts_9b_l20.jsonl \
  --mapping artifacts/qwen2.5-7b/axbench_diverse6/results/axbench_diverse6_mapping.jsonl \
  --concept-ids 9,10,52,380,395,419 --n-prompts 12 --n-samples 5 \
  --alphas 0.5,0.75,1.0 --random-seeds 17,42,101,314,2718 \
  --save-vectors-dir "$NLA_VECTORS/axbench_diverse6" --resume \
  --out "$NLA_RESULTS/axbench_diverse6.json"
```

### Gemma concept 3 and six-concept expansion

Stop Qwen, start Gemma as shown above, then:

```bash
source /workspace/nla/gemma3-12b.env

python -m experiments.runner axbench \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" --layer 32 \
  --metadata experiments/configs/axbench_concepts_9b_l20.jsonl \
  --mapping artifacts/gemma3-12b/full_run/results/axbench_c3_broad_mapping.jsonl \
  --concept-ids 3 --n-prompts 12 --n-samples 5 \
  --alphas 0.1,0.2,0.3 --random-seeds 17,42,101,314,2718 \
  --save-vectors-dir "$NLA_VECTORS/axbench_c3_lowalpha" --resume \
  --out "$NLA_RESULTS/axbench_c3_lowalpha.json"

python -m experiments.runner axbench \
  --target "$NLA_TARGET" --av "$NLA_AV" --ar "$NLA_AR" --layer 32 \
  --metadata experiments/configs/axbench_concepts_9b_l20.jsonl \
  --mapping artifacts/cross_model_extended_2026-08-08/gemma/results/axbench_diverse6_mapping.jsonl \
  --concept-ids 9,10,52,380,395,419 --n-prompts 12 --n-samples 5 \
  --alphas 0.1,0.2,0.3 --random-seeds 17,42,101,314,2718 \
  --save-vectors-dir "$NLA_VECTORS/axbench_diverse6" --resume \
  --out "$NLA_RESULTS/axbench_diverse6.json"
```

Do not overwrite files under `artifacts/`; use `/workspace/nla/results` for
new runs and archive them only after inspection.

## 8. Jacobian-lens sequence

Set the optional package path:

```bash
export PYTHONPATH=/workspace/steering/jacobian-lens
```

The recommended recovery path is to reuse the committed fitted lenses:

```text
Qwen:  artifacts/qwen2.5-7b/axbench_c3_broad12/checkpoints/c3_broad12_lens.pt
Gemma: artifacts/gemma3-12b/full_run/checkpoints/c3_broad12_lens.pt
```

Their fit checkpoints and exact 12 prompts are stored beside them. To refit
instead, turn a saved JSONL prompt file into the runner's pipe-separated input:

```bash
PROMPTS=$(python -c 'import json,sys; print("|".join(json.loads(x)["prompt"] for x in open(sys.argv[1])))' \
  artifacts/qwen2.5-7b/axbench_c3_broad12/results/lens_prompts.jsonl)

python -m experiments.runner jspace --action fit \
  --target /workspace/nla/models/qwen2.5-7b/target --layer 20 \
  --prompts "$PROMPTS" --lens /workspace/nla/checkpoints/qwen2.5-7b/c3_broad12_lens.pt
```

Use the Gemma prompt file, target, layer 32, and output path for a Gemma refit.

### Corrected Qwen magnitude-preserving ablation

```bash
python -m experiments.runner jspace --action ablate \
  --target /workspace/nla/models/qwen2.5-7b/target --layer 20 \
  --lens artifacts/qwen2.5-7b/axbench_c3_broad12/checkpoints/c3_broad12_lens.pt \
  --vector artifacts/qwen2.5-7b/axbench_c3_broad12/vectors/c3.ar_delta.pt \
  --prompt 'What is braising? Explain the technique and give a practical example.' \
  --concept 'casinos, gambling, betting, poker, roulette' \
  --alpha 0.75 --n-samples 30 \
  --out /workspace/nla/results/qwen2.5-7b/jspace_c3_broad12_ablation_magnitude_preserving.json
```

`experiments.runner` now carries projection/complement norm into effective
alpha. Older files named `normalized-components` and the original Qwen broad
ablation are diagnostic equal-norm tests, not magnitude-preserving conclusions.

### Seven-vector token readout

```bash
NAMES=$(python -c 'import json; print(",".join(json.load(open("experiments/configs/qwen_jspace_vectors.json")).keys()))')
VECTORS=$(python -c 'import json; print(",".join(json.load(open("experiments/configs/qwen_jspace_vectors.json")).values()))')

python -m experiments.jspace_readout \
  --target /workspace/nla/models/qwen2.5-7b/target \
  --lens artifacts/qwen2.5-7b/axbench_c3_broad12/checkpoints/c3_broad12_lens.pt \
  --layer 20 --vectors "$VECTORS" --names "$NAMES" \
  --terms-json experiments/configs/concept7_terms.json \
  --prompts 'Explain how photosynthesis supports ecosystems.|Describe the causes and consequences of inflation.|Give practical advice for maintaining a bicycle.|Summarize how local governments provide public services.' \
  --alpha 0.01 --top-k 50 --report-tokens 25 \
  --out /workspace/nla/results/qwen2.5-7b/jspace_concept_readout.json
```

For Gemma, load `experiments/configs/gemma_jspace_vectors.json`, use the
committed Gemma lens/target, layer 32, and a Gemma output path.

### Cross-concept geometry versus steering lift

```bash
python -m experiments.jspace_concepts \
  --lens artifacts/qwen2.5-7b/axbench_c3_broad12/checkpoints/c3_broad12_lens.pt \
  --layer 20 --vectors-json experiments/configs/qwen_jspace_vectors.json \
  --terms-json experiments/configs/concept7_terms.json \
  --results artifacts/qwen2.5-7b/axbench_c3_broad12/results/axbench_c3_broad.json,artifacts/qwen2.5-7b/axbench_diverse6/results/axbench_diverse6.json \
  --alpha 0.75 --out /workspace/nla/results/qwen2.5-7b/jspace_cross_concept.json

python -m experiments.jspace_concepts \
  --lens artifacts/gemma3-12b/full_run/checkpoints/c3_broad12_lens.pt \
  --layer 32 --vectors-json experiments/configs/gemma_jspace_vectors.json \
  --terms-json experiments/configs/concept7_terms.json \
  --results artifacts/gemma3-12b/full_run/results/axbench_c3_lowalpha.json,artifacts/cross_model_extended_2026-08-08/gemma/results/axbench_diverse6.json \
  --alpha 0.2 --out /workspace/nla/results/gemma3-12b/jspace_cross_concept.json
```

## 9. Reframing sequence

These commands reconstruct lexical, abstract, and behavioral casino directions
against neutral explanations, save the vectors, and evaluate three random
controls plus unsteered generation.

```bash
python -m experiments.reframing \
  --target /workspace/nla/models/qwen2.5-7b/target \
  --ar /workspace/nla/models/qwen2.5-7b/ar --layer 20 \
  --mapping artifacts/qwen2.5-7b/axbench_c3_broad12/results/axbench_c3_broad_mapping.jsonl \
  --concept-id 3 --n-prompts 12 --n-samples 5 --max-new-tokens 64 \
  --alpha 0.75 --random-seeds 17,42,101 \
  --vectors-dir /workspace/nla/vectors/qwen2.5-7b/reframing_c3 \
  --out /workspace/nla/results/qwen2.5-7b/reframing_c3.json

python -m experiments.reframing \
  --target /workspace/nla/models/gemma3-12b/target \
  --ar /workspace/nla/models/gemma3-12b/ar --layer 32 \
  --mapping artifacts/gemma3-12b/full_run/results/axbench_c3_broad_mapping.jsonl \
  --concept-id 3 --n-prompts 12 --n-samples 5 --max-new-tokens 64 \
  --alpha 0.2 --random-seeds 17,42,101 \
  --vectors-dir /workspace/nla/vectors/gemma3-12b/reframing_c3 \
  --out /workspace/nla/results/gemma3-12b/reframing_c3.json
```

## 10. User-turn versus assistant-turn sequence

Run both equal-energy and constant-per-token modes. The fixed-last-token run is
the AxBench-style calibration. This Qwen example is exact:

```bash
COMMON="--target /workspace/nla/models/qwen2.5-7b/target --av /workspace/nla/models/qwen2.5-7b/av --ar /workspace/nla/models/qwen2.5-7b/ar --layer 20"
VECTOR=artifacts/qwen2.5-7b/axbench_c3_broad12/vectors/c3.ar_delta.pt
PROMPT='What is braising? Explain the technique and give a practical example.'
POSITIONS=user_begin,user_response,user_end,assistant_begin,assistant_response

python -m experiments.runner sweep $COMMON \
  --concept 'casinos, gambling, betting, poker, roulette' --prompt "$PROMPT" \
  --vector "$VECTOR" --positions "$POSITIONS" --alphas 0.75 \
  --random-seeds 17,42,101 --n-samples 20 --max-new-tokens 64 \
  --energy-matched \
  --out /workspace/nla/results/qwen2.5-7b/turn_position_c3_energy_matched.json

python -m experiments.runner sweep $COMMON \
  --concept 'casinos, gambling, betting, poker, roulette' --prompt "$PROMPT" \
  --vector "$VECTOR" --positions "$POSITIONS" --alphas 0.75 \
  --random-seeds 17,42,101 --n-samples 20 --max-new-tokens 64 \
  --out /workspace/nla/results/qwen2.5-7b/turn_position_c3_constant_per_token.json

python -m experiments.runner sweep $COMMON \
  --concept 'casinos, gambling, betting, poker, roulette' --prompt "$PROMPT" \
  --vector "$VECTOR" --positions last --alphas 0.75 \
  --random-seeds 17,42,101 --n-samples 20 --max-new-tokens 64 \
  --out /workspace/nla/results/qwen2.5-7b/turn_position_c3_last_calibration.json
```

For Gemma, replace profile paths, use layer 32, vector
`artifacts/gemma3-12b/full_run/vectors/axbench_c3_lowalpha/c3.ar_delta.pt`,
alpha 0.2, and Gemma output paths.

## 11. Consolidated findings

### Qwen2.5-7B

- Grounded reward AV editing and nautical AR-delta steering demonstrate that
  the target/AV/AR/intervention stack works. Some reward variants saturate and
  cannot discriminate steering.
- Rabbit-to-mouse poetry failed; it is not a successful replication.
- Casino concept 3 is the strongest proofpoint: 85% strict hits at alpha 0.75
  over 12 prompts x 5 samples, versus 0% unsteered and at most 1.7% random.
- Five of six diverse concepts clearly steer at alpha 0.75. Gorilla is weak.
- The corrected magnitude-preserving broad-lens ablation is full 63.3%, top-32
  projection 0%, and complement 0%. Neither component alone is sufficient.
- Seven-vector J-space geometry has weak correlation with steering lift
  (Spearman 0.286 projection fraction; 0.321 Jacobian alignment).
- Jacobian-predicted casino tokens look semantically right, but actual
  small-alpha logit shifts align poorly (mean cosine 0.075).
- Reframing scores lexical 16.7%, abstract 6.7%, behavioral 20%, controls 0%.
- Constant-per-token assistant-response steering scores 65%; user-side sections
  score 0%; fixed final prompt token scores 60%. Equal-energy sections are null.

### Gemma 3 12B

- The pipeline is compatible and steering is real, but useful alphas are much
  lower than Qwen's. Qwen-scale alphas often cause repetition/collapse.
- Grounded reward is saturated and inconclusive. Rabbit-to-mouse poetry fails.
  Nautical AR-delta steering is strong.
- Casino concept 3 reaches 68.3% at alpha 0.2 and 88.3% at alpha 0.3, with all
  unsteered/random controls at 0% in that run.
- The six-concept expansion shows all six beyond controls at some alpha. At
  alpha 0.2: nighttime 98.3%, surgery 41.7%, music 75%, elections 40%, gorillas
  53.3%, chemistry 26.7%. Alpha 0.3 strengthens all six but is more intrusive.
- The fitted Gemma lens gives materially better local logit readouts than Qwen;
  casino-family predicted and actual tokens agree, with mean cosine 0.474.
- Seven-concept geometry correlations are moderately positive (0.643 and
  0.607) but n=7 is exploratory, selected, and not predictive evidence.
- Reframing scores lexical 85%, behavioral 55%, abstract 0%, controls 0%, even
  though the direction cosines are high.
- Constant-per-token assistant-response and fixed-last steering both score 95%;
  user-side sections and equal-energy sections score 0%.

### What has and has not been replicated

The experiments establish direction-specific steering proofpoints on Qwen and
Gemma, saved/reusable AR vectors, limited AxBench generalization, local
Jacobian-token readouts, and a positional assistant-response effect. They do
not replicate the complete NLA paper, full AxBench, Anthropic's private Claude
activations, or a general NLA--J-space theory. Do not generalize the selected
seven-concept correlations without broader concepts, prompts, generations,
layers, and independent lenses.

## 12. Known pitfalls

- Qwen must use layer 20 checkpoints; Gemma 12B must use layer 32 checkpoints.
- Preserve `HF_TOKEN_PATH` before changing `HF_HOME`; the setup script does so.
- Keep SGLang at `--mem-fraction-static 0.35` on one 80 GB A100.
- Gemma needs `--cuda-graph-backend-prefill disabled` for the observed SGLang
  ragged-prefill failure; the setup script supplies it.
- `apply_chat_template` may return `tokenizers.Encoding`; `chat_ids` converts it
  to a plain token-ID list.
- Empty template sections must use integer index tensors; this is fixed in
  `experiments/sections.py`.
- Random directions are specificity controls, not quality controls. Seed 17
  sometimes causes very short/corrupted generations at larger alpha.
- Alpha 0.3 Gemma and alpha 0.75--1.0 Qwen often insert concepts intrusively.
- The surgery lexicon includes broad terms such as `operation` and `dressing`;
  inspect generations, especially at alpha 0.2.
- Do not report old normalized-component ablations as magnitude preserving.
- Always inspect `*.case_study.md`; a strict hit can coexist with severe answer
  degradation or keyword flooding.

## 13. Final recovery checklist

Before releasing an instance:

```bash
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
(cd artifacts/cross_model_extended_2026-08-08 && sha256sum -c SHA256SUMS)
```

On a future machine:

1. Clone the GitHub fork.
2. Verify all bundle checksums.
3. Accept the Gemma license and run `hf auth login`.
4. Run `scripts/vast_setup.sh` for the required profile.
5. Install the pinned Jacobian-lens fork only for J-space work.
6. Reuse committed mappings, vectors, and fitted lenses unless deliberately
   testing a refit.
7. Write new outputs under `/workspace/nla`, never over archived evidence.

After the final guide commit is pushed, GitHub plus the public checkpoint IDs
above are sufficient to reconstruct the full experiment environment and retain
all irreplaceable outputs from this A100.
