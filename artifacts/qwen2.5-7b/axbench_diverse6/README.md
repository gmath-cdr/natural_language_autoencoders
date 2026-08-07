# Qwen2.5-7B diverse AxBench expansion

This bundle preserves the six-concept Qwen AxBench expansion completed on
2026-08-07. It tests whether the earlier casino/gambling result generalizes to
different semantic types without running full AxBench.

## Protocol

- Concepts: nighttime, surgery/wounds, music, elections, gorillas, and
  sodium/potassium/lithium/magnesium chemistry.
- 12 held-out prompts per concept.
- 5 generations per prompt and arm.
- Alphas: 0.5, 0.75, and 1.0.
- Controls: unsteered plus random-vector seeds 17, 42, 101, 314, and 2718.
- One saved AR-delta vector per concept.
- 19 arms and 1,140 generations per concept; 6,840 generations total.
- Strict metrics use the concrete lexicons saved in
  `results/axbench_diverse6_protocol.json`.

The strict analysis reports both generation-level hit rate and prompt-level
coverage so a pooled effect cannot be mistaken for broad prompt coverage.

## Strict-hit results

Each table entry is `NLA / highest random / unsteered`.

| Concept | Alpha 0.5 | Alpha 0.75 | Alpha 1.0 |
|---|---:|---:|---:|
| Nighttime | 5.0 / 0.0 / 0.0% | 63.3 / 0.0 / 0.0% | 68.3 / 0.0 / 0.0% |
| Surgery/wounds | 10.0 / 5.0 / 3.3% | 76.7 / 3.3 / 3.3% | 100.0 / 5.0 / 3.3% |
| Music | 13.3 / 3.3 / 3.3% | 48.3 / 3.3 / 3.3% | 70.0 / 3.3 / 3.3% |
| Elections | 36.7 / 11.7 / 8.3% | 100.0 / 13.3 / 8.3% | 100.0 / 10.0 / 8.3% |
| Gorillas | 0.0 / 0.0 / 0.0% | 5.0 / 0.0 / 0.0% | 15.0 / 0.0 / 0.0% |
| Alkali/electrolyte chemistry | 11.7 / 0.0 / 0.0% | 78.3 / 0.0 / 0.0% | 91.7 / 0.0 / 0.0% |

At alpha 0.75, prompt-level coverage was:

| Concept | Any hit among five samples | Majority of samples hit |
|---|---:|---:|
| Nighttime | 12/12 | 9/12 |
| Surgery/wounds | 10/12 | 10/12 |
| Music | 9/12 | 6/12 |
| Elections | 12/12 | 12/12 |
| Gorillas | 2/12 | 0/12 |
| Alkali/electrolyte chemistry | 12/12 | 10/12 |

## Interpretation

Five of the six new concepts move clearly beyond both unsteered and all five
random-vector controls. This extends the earlier gambling result to nighttime,
medical, music, civic, and chemistry concepts. Gorilla steering is weak and is
not a convincing success under this protocol.

This is directional concept insertion, not necessarily useful or
quality-preserving behavior. Sample inspection shows that the inserted concepts
often corrupt otherwise factual answers. At alpha 1.0, several concepts become
repetitive keyword floods:

- Elections rises from 8.25 strict terms per response at alpha 0.75 to 34.28 at
  alpha 1.0.
- Chemistry rises from 4.67 to 14.85.
- Surgery rises from 2.88 to 9.68.
- Music rises from 2.45 to 6.27.
- Nighttime alpha 1.0 also shows obvious repetition despite only a modest
  increase in hit rate.

## Alpha guidance from this run

- Nighttime: alpha 0.75 is the clearest tested tradeoff; alpha 1.0 degrades.
- Surgery/wounds: alpha 0.75 is strong, but already intrusive.
- Music: alpha 0.75 is moderate; alpha 1.0 is stronger but substantially more
  repetitive.
- Elections: alpha 0.5 is the least destructive tested setting; alpha 0.75 and
  1.0 oversteer badly.
- Gorillas: no useful alpha was found.
- Chemistry: alpha 0.5 is weak and alpha 0.75 is strong but intrusive; an
  intermediate follow-up around 0.6-0.65 is justified.

Overall, alpha 0.75 is a reliable *detection* setting for five concepts, but it
should not be interpreted as a generally quality-preserving operating point.

## Bundle layout

- `results/axbench_diverse6.json`: canonical 114-arm generation result.
- `results/axbench_diverse6.case_study.md`: all inspectable generations.
- `results/axbench_diverse6_mapping.jsonl`: 72 held-out prompt mappings.
- `results/axbench_diverse6_protocol.json`: concept IDs, exact lexicons, seeds,
  alphas, and sample counts.
- `results/axbench_diverse6_strict_metrics.json`: generation- and prompt-level
  strict metrics for every arm.
- `vectors/`: six saved AR-delta vectors.
- `SHA256SUMS`: integrity hashes for every archived payload.

No model weights were downloaded or changed for this run.
