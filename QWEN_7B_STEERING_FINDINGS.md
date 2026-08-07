# Qwen-7B steering findings

Status as of 2026-08-07.

## Artifact and backup status

All important Qwen experiment artifacts are pushed to GitHub. A checksum audit
matched every one of the 41 live files under the Qwen checkpoint, vector, and
result directories to a Git-tracked archive copy.

- Five lens/checkpoint files, including resumable and failed-fit checkpoints.
- Two local vector paths.
- Thirty-four result, mapping, and case-study files.
- Total archived Qwen footprint: approximately 223 MB.
- Complete broad concept-3 bundle: `artifacts/qwen2.5-7b/axbench_c3_broad12/`.
- Earlier complete run archive: `artifacts/qwen2.5-7b/full_run/`.

Downloaded model weights, the Hugging Face cache, server logs, and PID files are
intentionally excluded. They are operational data rather than experiment
artifacts.

## Overall finding

Steering clearly occurs on Qwen, but it is task-dependent. The strongest
evidence comes from a grounded reward-function AV edit and two independently
tested AR-delta concepts: nautical language and AxBench concept 3, terms related
to online gambling and casinos.

| Experiment | Result | Assessment |
|---|---|---|
| Grounded reward AV edit | Odd outputs rose from 15% unsteered to 80% at alpha 0.5 and 100% at alpha 0.75 | Successful AV-edit steering |
| Nautical AR-delta | 95% nautical-term incidence at alpha 0.75 versus 0% unsteered and at most 15% random | Successful concept steering |
| AxBench casino AR-delta | 85% casino/gambling incidence at alpha 0.75 versus 0% unsteered and at most 1.7% random | Strongest replication result |
| Rabbit-to-mouse poetry | No mouse outputs across three prompt variants and alphas through 4.0 | Failed |
| J-space | The result changed substantially after fitting a broader lens | Informative, but not generalizable |

These results support a credible Qwen steering proof. They do not constitute a
complete replication of the NLA paper.

## 1. Reward-function steering

The original small reward run was not reliable. It used only three generations
per arm and moved in the wrong direction: the intended even-to-odd NLA edit
produced 100% even outputs.

Follow-up diagnostics identified two problems:

- Some prompts were already saturated toward odd answers, leaving no room to
  detect steering.
- The AV explanation needed to be grounded at the token representing the parity
  condition.

The improved verbose grounded experiment worked:

| Alpha | AV even-to-odd | Unsteered | Highest random control |
|---:|---:|---:|---:|
| 0.25 | 52.6% odd | 15% | 35% |
| 0.50 | 80% odd | 15% | 35% |
| 0.75 | 100% odd | 15% | 60% |

This is a dose-responsive AV-edit result that exceeds every random control.
Direct AR steering was less consistent and produced more invalid outputs at
higher alpha.

Conclusion: AV editing can work on Qwen, but token placement and a
non-saturated prompt are crucial.

## 2. Rabbit-to-mouse poetry

Three poetry variants were tested, including blog-style and constrained
couplet prompts. None produced the target word `mouse`, even at alpha 2 or 4.
The generations remained about rabbits, bunnies, carrots, and similar animals.
Random controls behaved similarly.

The AV explanations were also poorly grounded in the actual prompt, which
likely made the resulting edit direction weak or irrelevant.

Conclusion: this proofpoint did not replicate on Qwen.

## 3. Nautical AR-delta steering

The preliminary three-sample sweep was inconclusive, but the controlled
replications succeeded. In the 20-sample run with three independently seeded
random directions:

| Alpha | NLA nautical hit rate | Highest random | Unsteered |
|---:|---:|---:|---:|
| 0.25 | 15% | 0% | 0% |
| 0.50 | 85% | 5% | 0% |
| 0.75 | 95% | 15% | 0% |

The NLA generations introduced ships, sailboats, lighthouses, harbors,
coastlines, and related language. Controls largely retained the original
tranquil-lake description.

At alpha 1.0 in the smaller replication, nautical language became highly
repetitive and degraded into sail/lighthouse loops. The useful range appears
closer to alpha 0.5-0.75.

Conclusion: a clear, repeatable AR-delta steering effect with a sensible dose
response, alongside evidence that excessive alpha harms quality.

## 4. AxBench concept 3: casinos and gambling

The first two-prompt spot check showed an effect at alpha 0.75:

- NLA built-in concept score: 1.87.
- Unsteered and three random controls: 1.0.

The broader replication used 12 held-out prompts, five generations per prompt,
five random-vector seeds, three alphas, and 1,140 total generations.

| Alpha | NLA strict hit rate | Highest random | Unsteered |
|---:|---:|---:|---:|
| 0.50 | 18.3% | 0% | 0% |
| 0.75 | 85% | 1.7% | 0% |
| 1.00 | 100% | 0% | 0% |

The saved broad-run vector is byte-identical to the original spot vector,
confirming deterministic reconstruction and the resumable workflow.

At alpha 1.0, the model averaged roughly 26 gambling terms per response and
often produced obvious keyword flooding. Alpha 0.75 is convincing directionally
but still fairly intrusive.

Conclusion: this is the strongest Qwen result. The NLA direction produces the
intended concept far more often than unsteered and multiple random controls.

## 5. J-space geometry and ablation

The tiny two-prompt lens initially suggested:

- Top-32 projection fraction: 0.173.
- The full vector worked.
- The projection did not.
- The complement retained most of the effect.

That suggested the behavior was predominantly outside the top-32 subspace.

The 12-prompt lens refit produced a different result:

- Top-32 projection fraction: 0.251.
- Full vector: 70% strict-hit rate and 5.10 terms per response.
- Top-32 projection: 90% and 3.13 terms per response.
- Complement: 0% and no matched terms.

The tiny-lens conclusion therefore did not survive. Under the broader fitted
lens, the top-32 projection carries the behavior while the complement does not.
The full vector has greater intensity when it activates, while the projection
activates more consistently.

Conclusion: the experiment demonstrates that J-space conclusions are highly
sensitive to lens fitting. It does not establish a general relationship between
NLA directions and J-space.

## Bottom line

Qwen steering is real and repeatable for:

- Grounded parity AV edits.
- Nautical AR-delta steering.
- AxBench casino/gambling AR-delta steering.

It failed or remained inconclusive for:

- Rabbit-to-mouse poetry.
- The original poorly grounded or saturated reward setups.
- The preliminary three-sample nautical sweep.

The evidence supports a credible Qwen steering proofpoint and a successful
single-concept AxBench replication. It does not yet establish broad AxBench
performance, replicate the complete NLA paper, or justify a general NLA-J-space
claim. Gemma has not been tested because its checkpoints are not locally
available.
