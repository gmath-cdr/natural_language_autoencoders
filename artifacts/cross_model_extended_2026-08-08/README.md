# Qwen/Gemma extended steering and J-space checks

This bundle preserves the 2026-08-08 follow-up experiments on Qwen2.5-7B and
Gemma 3 12B. It does not replace or overwrite any earlier archive. Model
weights are not included.

For restore/setup instructions and the exact experiment sequence, start at
`A100_REPRODUCTION_AND_RESULTS_GUIDE.md` in the repository root.

## Gemma six-concept AxBench expansion

Each concept used 12 held-out prompts, five samples per prompt, alphas
0.1/0.2/0.3, unsteered generation, and random-vector seeds 17, 42, 101, 314,
and 2718. That is 1,140 generations per concept and 6,840 total.

Each table entry is `NLA / highest random / unsteered` strict-hit percentage.

| Concept | alpha 0.1 | alpha 0.2 | alpha 0.3 |
|---|---:|---:|---:|
| Nighttime | 28.3 / 8.3 / 8.3 | 98.3 / 8.3 / 8.3 | 100.0 / 6.7 / 8.3 |
| Surgery/wounds | 0.0 / 0.0 / 1.7 | 41.7 / 0.0 / 1.7 | 96.7 / 0.0 / 1.7 |
| Music | 13.3 / 0.0 / 0.0 | 75.0 / 1.7 / 0.0 | 96.7 / 5.0 / 0.0 |
| Elections | 10.0 / 10.0 / 8.3 | 40.0 / 6.7 / 8.3 | 83.3 / 0.0 / 8.3 |
| Gorillas | 0.0 / 0.0 / 0.0 | 53.3 / 0.0 / 0.0 | 60.0 / 0.0 / 0.0 |
| Electrolyte/alkali chemistry | 0.0 / 0.0 / 0.0 | 26.7 / 0.0 / 0.0 | 85.0 / 0.0 / 0.0 |

All six concepts move beyond controls at some tested alpha. Alpha 0.2 is a
strong detection setting for nighttime, music, and gorillas, moderate for
surgery and elections, and weak for chemistry. Alpha 0.3 makes all six clear,
but median target-term counts of 3.5--8 for most concepts show increasing
intrusiveness and saturation. The surgery lexicon includes broad words such as
`operation` and `dressing`, so its low-count alpha-0.2 hits deserve more caution
than its alpha-0.3 result, where 12/12 prompts have majority-sample hits and the
median is seven terms.

## Corrected Qwen J-space ablation

The earlier broad-12 Qwen projection/complement ablation passed each component
through a generator that normalized it to unit length. It therefore measured
equal-norm directional sufficiency, not a magnitude-preserving decomposition.

The corrected alpha-0.75 result on 30 generations is:

| Component | Norm | Effective alpha | Strict hit rate |
|---|---:|---:|---:|
| Full | 1.0000 | 0.7500 | 63.3% |
| Top-32 projection | 0.2505 | 0.1879 | 0.0% |
| Complement | 0.9681 | 0.7261 | 0.0% |

Neither natural-magnitude component is independently sufficient in this
sample, even though the complement retains most vector norm. The full
combination appears necessary at this operating point. This invalidates the
older claim that the top-32 projection alone carries the behavior, but does not
establish whether the result is linear synergy, a nonlinear threshold, or
sampling variation.

## Jacobian token readouts

Four held-out prompts were used to compare Jacobian-predicted small-alpha logit
changes with actual intervention logit changes for seven vectors per model.

- Qwen mean predicted/actual cosine ranges from 0.002 to 0.317. For the casino
  vector, predicted top tokens include `casino`, `poker`, and `gambling`, but
  the actual finite-difference top tokens do not agree; mean cosine is 0.075.
- Gemma mean cosine ranges from 0.229 to 0.474. For the casino vector, predicted
  and actual top tokens are both dominated by casino/gambling terms; actual
  token ranks include `casino` rank 2, `casinos` rank 5, `gambling` rank 9,
  and `betting` rank 23.

Thus this fitted Gemma lens provides a materially better local unembedding
readout than the fitted Qwen lens. The JSON files retain top positive/negative
tokens, target-term ranks, prompt-level cosines, and top-50 overlap.

## Does J-space geometry predict steering success?

Across the seven selected concepts, exploratory Spearman correlations are:

| Model | Projection fraction vs strict lift | Jacobian alignment vs strict lift |
|---|---:|---:|
| Qwen | 0.286 | 0.321 |
| Gemma | 0.643 | 0.607 |

The Qwen association is weak. Gemma is moderately positive in this selected
seven-concept set, but n=7, one fitted layer/lens, and concept-specific alpha
calibration are far too limited for a predictive or general NLA--J-space claim.

## Lexical, abstract, and behavioral reframing

Each frame is an AR delta from three positive explanations against three
neutral explanations. Evaluation used 12 prompts, five samples per prompt,
three seeded random controls, and 64-token generations.

| Model | Lexical | Abstract | Behavioral | Highest random | Unsteered |
|---|---:|---:|---:|---:|---:|
| Qwen, alpha 0.75 | 16.7% | 6.7% | 20.0% | 0.0% | 0.0% |
| Gemma, alpha 0.2 | 85.0% | 0.0% | 55.0% | 0.0% | 0.0% |

Direction cosines are high (Qwen 0.76--0.81; Gemma 0.71--0.85), yet the
abstract frame is much less behaviorally effective, especially on Gemma. High
residual cosine therefore does not imply interchangeable steering behavior.
This experiment distinguishes wording classes but does not explain why the
abstract reframing fails.

## User-turn versus assistant-turn steering

One braising prompt, 20 samples per arm, three random controls, and 64-token
generations were used. Under equal total squared intervention energy, every
section was 0% on both models. Under constant per-token injection:

| Model | User begin/response/end | Assistant begin | Assistant response | Fixed final prompt token | Controls |
|---|---:|---:|---:|---:|---:|
| Qwen, alpha 0.75 | 0% | 0% | 65% | 60% | 0% |
| Gemma, alpha 0.2 | 0% | 0% | 95% | 95% | 0% |

Persistent decode-time assistant steering and the calibrated final prompt token
work; broader prompt-side sections do not. Equal-energy normalization divides
the coefficient by the square root of selected positions or generation
horizon and falls below the observed behavioral threshold. This is a
single-prompt positional spot check, not a universal chat-template conclusion.

## Layout and existing checkpoint references

- `gemma/results/axbench_diverse6*`: raw 6,840-generation expansion, prompt
  mapping, case study, and canonical strict metrics.
- `qwen/results/` and `gemma/results/`: readouts, geometry correlations,
  reframing, energy-matched/constant turn sweeps, and calibration controls.
- `qwen/vectors/` and `gemma/vectors/`: newly reconstructed reframing vectors
  and six Gemma AxBench vectors.
- `summary_metrics.json`: compact strict/readout/correlation metrics.
- `protocol/`: exact counts, alphas, seeds, positions, and lexicons.
- Qwen broad lens/vector remain at `artifacts/qwen2.5-7b/axbench_c3_broad12/`.
- Gemma broad lens/casino vector remain at `artifacts/gemma3-12b/full_run/`.

These results demonstrate real, direction-specific steering on both models and
answer the requested positional and local-token-readout spot checks. They do
not replicate the full NLA paper, full AxBench, or justify a general theory of
NLA/J-space correspondence.
