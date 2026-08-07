# Qwen2.5-7B concept-3 broader replication

This bundle preserves the expanded Qwen concept-3 AxBench and J-space run
completed on 2026-08-07. The target concept is **terms related to online
gambling and casinos**.

## Protocol

- AxBench: 12 held-out prompts, 5 generations per prompt and arm.
- Steering ratios: 0.5, 0.75, and 1.0.
- Controls: unsteered plus random-vector seeds 17, 42, 101, 314, and 2718.
- Lens: layer 20, fitted on 12 saved prompts rather than the earlier two.
- Geometry: top-32 right-singular-vector subspace.
- Ablation: alpha 0.75, 30 generations each for full, projection, and
  complement on a neutral braising prompt.

Exact machine-readable parameters are in `protocol.json`; exact evaluation and
lens prompts are also saved.

## AxBench result

The expanded run confirms concept-3 steering with a strong dose response. The
strict metric counts explicit gambling/casino terms, avoiding generic words in
the repository's built-in concept scorer.

| Alpha | AR built-in | AR strict hit rate | Highest random built-in | Highest random strict | Unsteered strict |
|---:|---:|---:|---:|---:|---:|
| 0.50 | 1.1133 | 18.3% | 1.0200 | 0.0% | 0.0% |
| 0.75 | 1.8067 | 85.0% | 1.0200 | 1.7% | 0.0% |
| 1.00 | 2.3333 | 100.0% | 1.0400 | 0.0% | 0.0% |

Each arm contains 60 generations, for 1,140 total. The reconstructed broad-run
AR-delta is byte-identical to the original spot vector.

## J-space result

The 12-prompt lens gives a top-32 projection fraction of 0.2505 and Jacobian
alignment of 0.02746. The behavioral ablation is:

| Arm | Generations | Built-in score | Strict hit rate | Strict terms/response |
|---|---:|---:|---:|---:|
| Full | 30 | 1.4267 | 70.0% | 5.10 |
| Top-32 projection | 30 | 1.4667 | 90.0% | 3.13 |
| Complement | 30 | 1.0000 | 0.0% | 0.00 |

This materially overturns the tiny two-prompt lens observation: under the
broader fitted lens, the top-32 projection retains the behavior and the
complement does not. The full vector produces more gambling terms when it
activates, while the projection activates on more generations.

## Interpretation boundary

This supports Qwen concept-3 steering relative to unsteered and five seeded
random controls. It does **not** establish a general NLA–J-space relationship:
the ablation still covers one model, concept, layer, subspace rank, alpha, and
generation prompt. Replicate across prompts, concepts, ranks, layers, and
models before generalizing.

Downloaded model weights are excluded and no checkpoint identifier was
changed. `SHA256SUMS` provides integrity hashes for every payload.
