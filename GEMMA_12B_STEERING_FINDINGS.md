# Gemma 3 12B NLA steering spot-check findings

This report summarizes the Gemma-only pipeline run performed on one 80 GB
A100. It uses the released, matching layer-32 checkpoints:

- target: `google/gemma-3-12b-it`
- AR: `kitft/nla-gemma3-12b-L32-ar`
- AV: `kitft/nla-gemma3-12b-L32-av`

The archived Qwen artifacts were not changed. Gemma outputs are under
`artifacts/gemma3-12b/full_run/`.

## Overall result

Gemma steering is clearly present, but Gemma needs a substantially lower
intervention coefficient than Qwen. At Qwen's useful alpha range, Gemma moves
strongly toward the target concept but collapses into repetitive casino text.
For AxBench concept 3, alpha 0.2 is the best tested compromise.

| Experiment | Result | Assessment |
|---|---|---|
| Technical reward smoke | Target, AV, AR, intervention, and generation completed | Compatibility passed |
| Grounded reward edit | Unsteered was already 100% odd (`77` in 20/20) | Saturated and inconclusive |
| Rabbit-to-mouse poetry | 0/20 mouse hits for NLA and controls at alpha 0.5, 0.75, and 1.0 | Failed |
| Nautical AR-delta | 100% strict hits at alpha 0.5 and 0.75 versus 0% unsteered and random controls | Strong steering, with random-control corruption |
| AxBench concept 3, high alpha | 96.7%, 90%, and 100% strict hits at alpha 0.5, 0.75, and 1.0; all controls 0% | Strong but unusably repetitive |
| AxBench concept 3, low alpha | 0%, 68.3%, and 88.3% strict hits at alpha 0.1, 0.2, and 0.3; all controls 0% | Useful range begins near 0.2 |
| Broad-12 J-space geometry | Top-32 projection fraction 0.0198 | Direction is mostly outside this fitted top-32 subspace |
| Corrected J-space ablation at alpha 0.2 | Full 70%, projection 0%, complement 90% strict hits | Local spot result only |

## Interpretation

The strongest evidence is AxBench concept 3. Across 12 held-out prompts and
five samples per prompt, unsteered and all five seeded random directions had
zero strict casino/gambling hits. The NLA AR-delta produced 68.3% hits at
alpha 0.2 and 88.3% at alpha 0.3. Alpha 0.3 already showed growing repetition;
alpha 0.5 and above frequently degraded into casino loops.

The nautical test independently supports steering: NLA rose from 0% unsteered
to 10% at alpha 0.25 and 100% at alpha 0.5 and 0.75, while all three seeded
random controls remained at 0%. Some random directions severely damaged
fluency, so random controls establish direction specificity but are not a
quality baseline by themselves.

The reward proofpoint cannot discriminate steering on Gemma because the base
model is saturated toward the desired odd answer. Poetry did discriminate but
was negative: every arm completed the rabbit rhyme unchanged.

## J-space caution

The lens was fitted at layer 32 using 12 semantically diverse, length-normalized
held-out prompts. Only 1.98% of the unit AR-delta norm lies in its top-32 right
singular subspace. A magnitude-preserving ablation gave 0% strict hits for the
projection and retained the effect in the complement.

This does not support a general NLA--J-space conclusion. It applies only to
this model, layer, concept, lens rank, prompt corpus, and sampling run. The
archived `*.normalized-components.*` files preserve an earlier diagnostic run
that incorrectly renormalized each component to unit length; they must not be
used as the reported ablation.

## Bottom line

Gemma 3 12B does steer, and the concept-3 effect is stronger than controls,
but it is not simply better than Qwen. It is more sensitive to alpha: the
Qwen-scale intervention oversteers badly, while alpha around 0.2 produces a
credible targeted effect with materially better answer coherence.

## Extended cross-model follow-up (2026-08-08)

The six-concept Gemma expansion completed 6,840 generations. All six concepts
move beyond controls at some tested alpha. At alpha 0.2, strict hit rates are
98.3% nighttime, 41.7% surgery/wounds, 75.0% music, 40.0% elections, 53.3%
gorillas, and 26.7% electrolyte/alkali chemistry. Alpha 0.3 raises them to
83.3--100% except gorillas at 60%, but is more intrusive.

The seven-vector token readout aligns predicted and actual casino-family logit
changes substantially better than Qwen. Exploratory J-space geometry has a
0.643 Spearman correlation with strict lift, but only over seven selected
concepts. Lexical and behavioral casino reframings score 85% and 55%; the
abstract frame scores 0% despite high direction cosine. Constant-per-token
assistant-response steering scores 95%, while user-side sections score 0%; an
equal-total-energy sweep is null everywhere.

Raw results, case studies, vectors, exact protocols, and cautions are archived
under `artifacts/cross_model_extended_2026-08-08/`.
