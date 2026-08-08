# Gemma 3 12B full steering spot-check archive

This directory contains the complete lightweight artifact set from the Gemma
3 12B layer-32 run. It intentionally excludes the downloaded Hugging Face model
weights, which remain in `/workspace/nla/models/gemma3-12b/` and exceed GitHub
file limits.

Included:

- all machine-readable result JSON and human-readable case studies;
- the exact concept-3 held-out prompt mapping;
- high- and low-alpha AxBench concept-3 sweeps;
- saved AR-delta vectors;
- the broad-12 Jacobian lens and resumable fit checkpoint;
- the preserved failed short-prompt fit checkpoint;
- corrected magnitude-preserving J-space geometry and ablation;
- the earlier normalized-component ablation retained only as a diagnostic;
- protocol metadata, lens prompts, and SHA-256 checksums.

See `GEMMA_12B_STEERING_FINDINGS.md` at the repository root for conclusions
and limitations.

