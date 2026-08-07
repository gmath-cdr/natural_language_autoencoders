# Complete Qwen2.5-7B run archive

This directory is the complete repository backup of the Qwen artifacts present
under `/workspace/nla` on 2026-08-07. It supplements the smaller curated
`axbench_c3_spot` bundle.

## Contents

- `checkpoints/c3_tiny_lens.pt`: final layer-20 J-space lens.
- `checkpoints/c3_tiny_lens.pt.fit-ckpt`: resumable lens-training checkpoint.
- `checkpoints/c3_tiny_lens.pt.fit-ckpt.failed-short-prompts`: retained failed
  short-prompt fit checkpoint for provenance and diagnosis.
- `vectors/c3.ar_delta.pt`: normalized concept-3 AR-delta vector.
- `results/`: every Qwen JSON, JSONL, and generated case-study artifact from
  the reward, poetry, nautical AR, AxBench concept-3, and J-space runs.
- `SHA256SUMS`: integrity hashes for every archived payload.

The resumable checkpoints are stored directly in Git because this public fork
does not accept newly uploaded Git LFS objects. Each file remains below
GitHub's per-file size limit. Downloaded model weights are intentionally
excluded: they are not experiment artifacts, and no model or checkpoint
identifier was changed while creating this archive.

## Interpretation boundary

The concept-3 spot check is successful, but the two-prompt J-space lens is too
small to support a general NLA–J-space conclusion. Refit on a substantially
broader prompt set and repeat the geometry and full/projection/complement
ablation with more generations before generalizing.
