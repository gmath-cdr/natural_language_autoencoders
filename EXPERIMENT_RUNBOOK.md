# NLA Steering Experiment Runbook

This is the operating guide for the inference-time steering experiments in
`experiments/`. Use it on a temporary A100 JupyterHub or Vast instance. Keep
all generated artifacts under one durable workspace such as `/mnt/nla`.

## Scope and one-A100 matrix

| Profile | One 80GB A100 workflow |
|---|---|
| Qwen2.5-7B, layer 20 | paper replications, sweeps, AxBench, J-space |
| Gemma-3-12B, layer 32 | sweeps, AxBench, small J-space fit |
| Gemma-3-27B, layer 41 | AR-delta/random/control sweeps and AxBench |
| Llama-3.3-70B, layer 53 | excluded: multi-GPU implementation required |

The Qwen reward and poetry experiments use AV-edit vectors. Do not schedule
the analogous AV-edit workflow for Gemma-27B on one A100: the AV server plus
AR model exceeds safe VRAM headroom. For AxBench and section sweeps, the runner
constructs AR vectors first, releases the AR, and then loads the target model.

## Persistent layout

```text
/mnt/nla/
  models/                 # local HF target, AV, and AR checkpoints
  results/qwen/           # JSON outputs
  vectors/qwen/           # saved .pt vectors/controls
  checkpoints/            # Jacobian lens files and fit checkpoints
```

Use a persistent disk or volume for `/mnt/nla`, but also back up to Drive. A
temporary A100 machine can be wiped when its allocation ends.

## Setup

```sh
git clone https://github.com/kitft/natural_language_autoencoders.git
cd natural_language_autoencoders
python -m pip install -e .
python -m pip install "sglang[all]>=0.5.6"
```

### Vast.ai one-command setup

For a Vast Docker/PyTorch instance with an idle **80GB A100** and a 200GB+
persistent volume, authenticate with Hugging Face and run the checked-in
bootstrap script. It stores the target, AV, AR, cache, logs, and artifacts on
the chosen volume; no token is written into the repository or the script.

```sh
hf auth login
bash scripts/vast_setup.sh --profile qwen2.5-7b --workspace /workspace/nla --gpu 0
```

For Gemma, first accept the base-model licence using the same Hugging Face
account, then run:

```sh
bash scripts/vast_setup.sh --profile gemma3-12b --workspace /workspace/nla --gpu 0
```

The script enables the current Hugging Face Xet high-performance transfer path,
resumes downloads, checks that the selected GPU has 80GB VRAM and 65GB free,
requires 110GB free for Qwen or 150GB for Gemma, starts the AV SGLang server,
and runs preflight. Re-run with `--skip-download` after a completed download;
use `--help` to see all options.

Run profiles sequentially on one GPU. Before starting Gemma after Qwen, stop
the Qwen AV server cleanly:

```sh
bash scripts/vast_setup.sh --profile qwen2.5-7b --workspace /workspace/nla --stop-server
```

Download the matching target, AV, and AR checkpoints under `/mnt/nla/models`.
For gated Gemma/Llama base models, authenticate with Hugging Face first. Keep
the three components from the same profile and extraction layer.

Launch SGLang for the AV checkpoint. It must use the exact AV path and disable
the radix cache:

```sh
python -m sglang.launch_server \
  --model-path /mnt/nla/models/qwen-av --port 30000 \
  --disable-radix-cache --trust-remote-code
```

## Preflight

Run this before any lengthy job:

```sh
python -m experiments.preflight \
  --target /mnt/nla/models/qwen-target \
  --av /mnt/nla/models/qwen-av \
  --ar /mnt/nla/models/qwen-ar \
  --sglang-url http://localhost:30000 --require-cuda
```

Syntax-only validation, useful on a laptop, is:

```sh
python -m py_compile experiments/*.py
```

## First A100 proofpoint

Run Qwen first. It validates target residual capture, AV decoding, edited AR
reconstruction, intervention hooks, controls, and atomic result output.

```sh
python -m experiments.runner reward \
  --target /mnt/nla/models/qwen-target --av /mnt/nla/models/qwen-av \
  --ar /mnt/nla/models/qwen-ar --layer 20 --alphas 0.5,1.0 \
  --n-samples 20 --out /mnt/nla/results/qwen/reward.json

python -m experiments.runner poetry \
  --target /mnt/nla/models/qwen-target --av /mnt/nla/models/qwen-av \
  --ar /mnt/nla/models/qwen-ar --layer 20 --alphas 0.5,1.0 \
  --n-samples 20 --out /mnt/nla/results/qwen/poetry.json
```

Success is a directional change in the NLA arm that exceeds both unsteered and
random controls. Treat this as a proofpoint, not a final statistical claim.

Each `reward` or `poetry` JSON now also creates a sibling
`*.case_study.md` file. It contains activation and delta norms, original and
edited AV explanations for every rollout, plus alpha-by-alpha raw samples in
the qualitative case-study format. Keep the JSON as the canonical checkpoint;
use the Markdown file for inspection and sharing.

All other experiment actions also emit a sibling `*.case_study.md`: section
sweeps and AxBench include per-arm metrics and raw samples; J-space geometry
includes its complete JSON metrics; J-space ablation includes metrics and raw
samples. Only AV-edit case studies include AV explanation and delta diagnostics,
because AR-delta/DiffMean/PCA experiments do not create an AV edit.

## Two-model spot suite: AxBench, J-space, and save tests

After the Qwen proofpoint, run this small protocol for **both Qwen-7B and
Gemma-12B** before starting the full benchmark. Substitute the matching local
target/AR/AV paths and layer (`20` for Qwen, `32` for Gemma-12B).

1. Start the 15-minute Drive watcher from the backup section below.
2. Run one AxBench concept, two prompts, three samples, one alpha, and save its
   AR-delta vector:

```sh
python -m experiments.runner axbench \
  --target /mnt/nla/models/qwen-target --av /mnt/nla/models/qwen-av \
  --ar /mnt/nla/models/qwen-ar --layer 20 \
  --metadata /data/axbench/metadata.jsonl --mapping /data/axbench/mapping.jsonl \
  --parquet /data/axbench/train_data.parquet --concept-ids 1 \
  --n-prompts 2 --n-samples 3 --alphas 1.0 \
  --save-vectors-dir /mnt/nla/vectors/qwen \
  --out /mnt/nla/results/qwen/axbench_spot.json
```

3. Verify that `axbench_spot.json` and `c1.ar_delta.pt` exist, then fit a tiny
   lens and run geometry/ablation against that vector:

```sh
python -m experiments.runner jspace --action fit \
  --target /mnt/nla/models/qwen-target --layer 20 \
  --lens /mnt/nla/checkpoints/qwen-spot-lens.pt \
  --prompts "A short test sentence.|Activation steering changes behavior."

python -m experiments.runner jspace --action geometry \
  --target /mnt/nla/models/qwen-target --layer 20 \
  --lens /mnt/nla/checkpoints/qwen-spot-lens.pt \
  --vector /mnt/nla/vectors/qwen/c1.ar_delta.pt \
  --out /mnt/nla/results/qwen/jspace_geometry_spot.json

python -m experiments.runner jspace --action ablate \
  --target /mnt/nla/models/qwen-target --layer 20 \
  --lens /mnt/nla/checkpoints/qwen-spot-lens.pt \
  --vector /mnt/nla/vectors/qwen/c1.ar_delta.pt \
  --concept "AxBench concept 1" --n-samples 3 \
  --out /mnt/nla/results/qwen/jspace_ablation_spot.json
```

Repeat with Gemma-12B paths, layer `32`, and separate `gemma12` result/vector/
lens paths. This is a save test because it produces an atomic AxBench JSON,
saved vector, saved lens, geometry JSON, ablation JSON, and an off-machine
Drive copy. It should take roughly 1–2 hours per model after checkpoints are
cached; do not use it as the final J-space estimate.

## Required execution order

When an A100 becomes available, do not start all profiles at once. Follow this
order:

1. Configure Drive backup and launch the matching Qwen AV SGLang server.
2. Run Qwen preflight and the Qwen proofpoint above.
3. Run Qwen sections, AxBench, and J-space; make a final Drive copy.
4. Stop the Qwen AV server and release cached Qwen models.
5. Launch the matching Gemma-12B AV server, run preflight, then run Gemma-12B
   sections, AxBench, and (if time permits) the small J-space fit.
6. Copy all artifacts to Drive and push the code before the allocation ends.

Qwen-7B is deliberately first: it is the fastest end-to-end validation of the
environment and checkpoint contract. Do not proceed to Gemma-12B if Qwen
preflight or the controlled Qwen proofpoint fails.

## Section sweep

```sh
python -m experiments.runner sweep \
  --target /mnt/nla/models/qwen-target --av /mnt/nla/models/qwen-av \
  --ar /mnt/nla/models/qwen-ar --layer 20 \
  --concept "references to video and multimedia content" \
  --prompt "Suggest a creative hobby for the weekend." --n-samples 10 \
  --out /mnt/nla/results/qwen/sections.json
```

The default sweep covers `last`, `user_begin`, `user_response`, `user_end`,
`assistant_begin`, and decode-time `assistant_response`.

## AxBench, shards, and resume

Run AxBench with a profile-matched target/AR pair. Each completed concept is
atomically written to the output JSON. After interruption, re-run with the
same output path and `--resume`.

```sh
python -m experiments.runner axbench \
  --target /mnt/nla/models/qwen-target --av /mnt/nla/models/qwen-av \
  --ar /mnt/nla/models/qwen-ar --layer 20 \
  --metadata /data/axbench/metadata.jsonl --mapping /data/axbench/mapping.jsonl \
  --n-prompts 12 --n-samples 10 --resume \
  --parquet /data/axbench/train_data.parquet \
  --out /mnt/nla/results/qwen/axbench.json
```

For parallel workers, use disjoint shards and separate output paths:

```sh
python -m experiments.runner axbench ... --num-shards 3 --shard-index 0 \
  --resume --out /mnt/nla/results/qwen/axbench.shard0.json
```

Merge non-overlapping JSON arms after all shards finish:

```python
from experiments.results import merge
merge(["/mnt/nla/results/qwen/axbench.shard0.json",
       "/mnt/nla/results/qwen/axbench.shard1.json",
       "/mnt/nla/results/qwen/axbench.shard2.json"],
      "/mnt/nla/results/qwen/axbench.json")
```

## J-space

Install `jacobian-lens` separately. Fit only on a full-precision target:

```sh
python -m experiments.runner jspace --action fit \
  --target /mnt/nla/models/qwen-target --layer 20 \
  --lens /mnt/nla/checkpoints/qwen-l20.pt
```

Then use `--action geometry` or `--action ablate` with a saved vector. Prefer
Qwen for J-space on one A100; Gemma-27B fitting is not recommended.

## Back up continuously

Configure Drive with `rclone config` and a remote called `gdrive`. Start this
in a separate terminal before running experiments:

```sh
python -m experiments.backup watch \
  /mnt/nla/results /mnt/nla/vectors /mnt/nla/checkpoints \
  --remote gdrive:algoverse/nla-a100-2026-08 --interval-minutes 15
```

Run one final copy before the allocation expires:

```sh
python -m experiments.backup copy \
  /mnt/nla/results /mnt/nla/vectors /mnt/nla/checkpoints \
  --remote gdrive:algoverse/nla-a100-2026-08
```

The backup command uses additive `rclone copy`, never destructive `sync`.
Back up code separately and explicitly after GitHub credentials are configured:

```sh
python -m experiments.backup git-push --message "Add NLA steering experiments"
```

## Review results

Produce a concise control-aware Markdown report after a sweep or AxBench run:

```sh
python -m experiments.report /mnt/nla/results/qwen/sections.json \
  --out /mnt/nla/results/qwen/sections_report.md
```

## Recovery checklist

1. Start the machine and remount the persistent volume.
2. Restore `/mnt/nla` from Drive if necessary.
3. Restart the matching AV SGLang server.
4. Run `experiments.preflight`.
5. Restart AxBench with exactly the same `--out` plus `--resume`.
6. Run a final Drive copy and Git push before the time window ends.
