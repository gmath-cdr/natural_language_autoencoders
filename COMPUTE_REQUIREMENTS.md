# Compute and storage requirements for NLA steering

Gemma 3 27B steering is feasible on one 80 GB A100 for AR-delta experiments,
but not the full AV-edit workflow. Llama 3.3 70B is not currently runnable with
this repository's one-GPU runner; it needs multi-GPU engineering first.

## What each GPU can run

| Experiment | One A100 80 GB | Notes |
|---|---:|---|
| Qwen 2.5 7B full NLA/AV/AR/J-space | Yes | Demonstrated in the archived experiments |
| Gemma 3 12B full NLA/AV/AR/J-space | Yes | Demonstrated in the archived experiments |
| Gemma 3 27B AR-delta steering, controls, and AxBench | Yes | Load AR, save the vector, unload AR, then load the target |
| Gemma 3 27B AV-edit reward/poetry workflow | No | The AV server and AR/target workloads exceed safe headroom |
| Gemma 3 27B substantial J-space fitting | Not recommended | Expected to be slow and memory-constrained |
| Llama 3.3 70B AR-delta steering | Not yet | Requires adapting model loading and hooks for multiple GPUs |
| Llama 3.3 70B AV editing | Not yet | Conservatively likely to need at least 4x80 GB for concurrent unquantized components |

This support matrix is also documented in
[`EXPERIMENT_RUNBOOK.md`](EXPERIMENT_RUNBOOK.md). The one-command bootstrap in
[`scripts/vast_setup.sh`](scripts/vast_setup.sh) currently provides profiles
only for Qwen 7B and Gemma 12B. Gemma 27B is supported conceptually by the
runner and runbook, but its setup profile must still be added or performed
manually. Use layer 41 and `--skip-server` for AR-delta-only work.

## Why the instance had a 220 GB disk

The run did not consume 220 GB. That was the volume's capacity. The following
was measured on the original instance on 2026-08-08:

| Item | Actual disk usage |
|---|---:|
| Entire filesystem | 113 GB |
| Qwen target + AR + AV | 39 GB |
| Gemma 12B target + AR + AV | 61 GB |
| All model directories combined | 99 GB |
| Main repository | 699 MB |
| AxBench repository | 731 MB |
| Jacobian-lens repository | 4.5 MB |
| Results | 20 MB |
| Saved vectors | 396 KB |
| Lens/checkpoint artifacts | 337 MB |
| pip cache | 3.2 GB |
| Free space remaining | 108 GB |

The additional capacity protected against temporary and resumable Hugging
Face/Xet downloads, holding Qwen and Gemma checkpoints simultaneously, Python
environments, package caches, interrupted downloads, and future outputs.

For only the existing Qwen and Gemma 12B results, approximately 150 GB total
could work if managed carefully. A 200--260 GB volume is more comfortable and
less prone to download failures.

## Storage for larger models

Gemma 27B is much larger than a single 27B target download because NLA uses
three different checkpoints:

| Gemma 27B component | Approximate download size |
|---|---:|
| Base target | 59 GB |
| AR checkpoint | 37.6 GB |
| AV checkpoint | 108 GB |
| Complete set | 205 GB |

The published sizes are visible in the
[Gemma 27B AR repository](https://huggingface.co/kitft/nla-gemma3-27b-L41-ar/tree/main)
and
[Gemma 27B AV repository](https://huggingface.co/kitft/nla-gemma3-27b-L41-av/tree/main).

The one-A100 AR-delta protocol needs only the target and AR checkpoint, or
approximately 97 GB. A fresh 150--180 GB disk should be sufficient. The 108 GB
that remained on the original instance is too marginal for a safe download
alongside all existing models.

For Llama 70B, the approximate sizes are:

| Llama 70B component | Approximate download size |
|---|---:|
| Base target | 141 GB |
| AV checkpoint | 141 GB |
| AR checkpoint | Roughly 100 GB |
| Complete set | Roughly 380 GB |

Provision at least 450--500 GB if retaining all three. The released
[Llama 70B AV checkpoint](https://huggingface.co/kitft/Llama-3.3-70B-NLA-L53-av/tree/main)
alone is 141 GB.

## Does it have to be an A100?

No. The workflow needs compatible CUDA hardware with sufficient VRAM. The
repository specifies A100 because that is the configuration tested end to end.

| GPU configuration | Suitable workload |
|---|---|
| 24 GB RTX 4090, A10, or L4 | Qwen AR-only experiments with smaller batches; the full workflow may be tight |
| 40--48 GB A100, L40S, or RTX A6000 | Qwen comfortably; Gemma 12B AR-only and some J-space work |
| 80 GB A100 | Full Qwen and Gemma 12B; Gemma 27B AR-only |
| 80 GB H100 | Same compatibility class and faster, but normally more expensive |
| 2x80 GB A100/H100 | Potential Llama 70B AR-only loading after multi-GPU support is implemented |
| 4x80 GB | Conservative target for unquantized Llama 70B AV plus AR workflows |
| 141 GB H200 | Large memory, but a 141 GB Llama checkpoint leaves little single-GPU runtime headroom |

Official specifications list 80 GB for the
[A100](https://www.nvidia.com/en-us/data-center/a100/), 48 GB for the
[L40S](https://www.nvidia.com/en-us/data-center/l40s/), and 141 GB for the
[H200](https://www.nvidia.com/en-us/data-center/h200/).

The current bootstrap rejects cards below approximately 70 GB even when a
smaller experiment could technically fit. Running on a 40--48 GB card requires
relaxing that guard and using `--skip-server` where appropriate.

## Cheapest sensible path

- For more Qwen experiments, use a 40--48 GB GPU and run AR-only or J-space
  workloads.
- For a full Gemma 12B reproduction, retain an A100 80 GB or another compatible
  80 GB NVIDIA GPU.
- For Gemma 27B, rent one 80 GB GPU, download only the target and AR checkpoint,
  and run AxBench/random-control steering at layer 41.
- For Llama 70B, add and test multi-GPU model loading and intervention hooks
  before renting the GPUs. Then begin with a 2x80 GB AR-only smoke test.
- Do not quantize the target or NLA checkpoints for the first cross-model
  comparison. Quantization can alter residual directions, so it would no longer
  be a like-for-like replication.
