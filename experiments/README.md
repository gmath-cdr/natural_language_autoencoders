# NLA Steering Experiments

This inference-only package composes the public upstream APIs:

- `nla_inference.NLAClient` for AV decoding through an SGLang server;
- `nla_inference.NLACritic` for AR reconstruction;
- a separately loaded target model for residual capture and steering hooks.

It does not modify NLA training, Miles, or SGLang. Start an SGLang server for
the matching AV checkpoint as described in `docs/inference.md`, then use the
experiment runner. Every AV, AR, target model, and layer must belong to the
same released checkpoint profile.

## Paper-style single-token replications

The runner captures the **real target-model residual**, asks the native AV to
describe it, edits the AV explanation, reconstructs both descriptions with the
native AR, and applies the resulting delta back at the original token. Results
are atomically checkpointed after every arm.

```sh
python -m experiments.runner reward \
  --target /models/qwen-target --av /models/qwen-av --ar /models/qwen-ar \
  --layer 20 --out results/reward.json
```

The `poetry` command implements the portable rabbit-to-mouse analogue. The
original Claude activation cannot be reproduced from an open Qwen checkpoint,
but the intervention procedure and controls are the same.

## Remaining experiment modules

- `profiles.py` — released Qwen, Gemma, and Llama checkpoint metadata.
- `vectors.py` — AR-delta, DiffMean, PCA, random, and AV-edit directions.
- `sections.py` — Qwen `user_*` / `assistant_*` token-resolvers, including
  decode-time `assistant_response` steering.
- `jspace.py` — optional Jacobian-lens fitting, geometry, and projection.
- `data.py`, `results.py` — AxBench loading, scoring, atomic checkpoints, and
  non-overlapping shard merge.

`jspace.py` imports `jacobian-lens` only when fitting/loading a lens; it is not
an upstream training dependency.

## Wired commands

```sh
# Token and section sweep with NLA and random controls.
python -m experiments.runner sweep --target /models/qwen --ar /models/qwen-ar \
  --av /models/qwen-av --layer 20 --concept "nautical imagery" \
  --prompt "Explain recursion." --out results/sections.json

# Full supplied AxBench metadata file; one deterministic resumable shard.
python -m experiments.runner axbench --target /models/qwen --ar /models/qwen-ar \
  --av /models/qwen-av --layer 20 --metadata metadata.jsonl --mapping mapping.jsonl \
  --num-shards 3 --shard-index 0 --resume --out results/axbench.shard0.json

# Optional J-space actions after installing jacobian-lens.
python -m experiments.runner jspace --action geometry --target /models/qwen \
  --layer 20 --lens results/lens.pt --vector results/c1.pt --out results/geometry.json
```

## One A100 80GB support matrix

| Profile | Single-token / sections / AxBench | Native AV-edit paper run | J-space fit |
|---|---|---|---|
| Qwen2.5-7B L20 | yes | yes | yes |
| Gemma-3-12B L32 | yes | feasible, but not a paper replication | yes, start with a small fit |
| Gemma-3-27B L41 | yes, AR-delta / random / supplied controls | no: AV server + AR exceeds one A100 | not recommended on one A100 |
| Llama-3.3-70B L53 | no | no | no |

For the three supported evaluation profiles, `sweep` and `axbench` construct
their AR vectors first, release the AR and CUDA cache, and only then load the
target model. This avoids concurrent AR+target residency on one A100.

## A100 backup workflow

Configure Google Drive once with `rclone config`, using a remote named
`gdrive`. Start the following in a separate Jupyter terminal before the
experiment. It copies every 15 minutes and is safe to rerun after a restart:

```sh
python -m experiments.backup watch results vectors checkpoints \
  --remote gdrive:algoverse/nla-a100-2026-08 --interval-minutes 15
```

Use `copy` for one final backup. It uses `rclone copy`, never `sync`, so it
does not delete anything already in Drive. Back up source code separately and
explicitly once GitHub credentials are configured:

```sh
python -m experiments.backup git-push --message "Add NLA steering experiments"
```

## Validate before renting

Syntax can be checked anywhere, even without an ML environment:

```sh
python -m py_compile experiments/*.py
```

On the A100, run the preflight before starting an experiment. It checks Python
packages, local target/AV/AR checkpoints and sidecars, CUDA, and the SGLang
health endpoint without loading a full target model:

```sh
python -m experiments.preflight --target /models/qwen --av /models/qwen-av \
  --ar /models/qwen-ar --sglang-url http://localhost:30000 --require-cuda
```
