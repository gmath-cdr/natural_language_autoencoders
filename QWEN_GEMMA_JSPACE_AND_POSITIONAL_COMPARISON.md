The two previously open questions are now experimentally addressed, although only as scoped spot checks—not general conclusions.

## Qwen versus Gemma steering

| Concept | Qwen α=0.75 | Gemma α=0.2 | Gemma α=0.3 |
|---|---:|---:|---:|
| Casino | 85.0% | 68.3% | 88.3% |
| Nighttime | 63.3% | 98.3% | 100% |
| Surgery/wounds | 76.7% | 41.7% | 96.7% |
| Music | 48.3% | 75.0% | 96.7% |
| Elections | 100% | 40.0% | 83.3% |
| Gorillas | 5.0% | 53.3% | 60.0% |
| Chemistry | 78.3% | 26.7% | 85.0% |

Qwen reliably steers five of the six expanded concepts at α=0.75, with gorillas remaining weak. Gemma steers all six, but its useful alpha is lower and more concept-dependent. At α=0.3 Gemma becomes strong across the set, but steering is frequently intrusive or repetitive.

Gemma is therefore not simply “better.” It is more sensitive: lower coefficients can produce large effects, while Qwen generally needs around α=0.75.

## Question 1: JLens / J-space interpretability

The old Qwen interpretation needs correction.

### Corrected Qwen ablation

The earlier result—projection 90%, complement 0%—renormalized both components to unit length. It demonstrated equal-norm directional sufficiency, not a natural-magnitude decomposition.

The corrected magnitude-preserving result is:

| Qwen component | Norm | Effective α | Strict hits |
|---|---:|---:|---:|
| Full vector | 1.000 | 0.750 | 63.3% |
| Top-32 projection | 0.251 | 0.188 | 0% |
| Complement | 0.968 | 0.726 | 0% |

Therefore, the claim that “the effective casino signal is substantially represented in the fitted top-32 J-space” is no longer supported by the corrected ablation. Neither component works independently at its natural magnitude; the complete vector appears necessary at this operating point.

### Gemma ablation

Gemma shows a different result:

| Gemma component | Strict hits |
|---|---:|
| Full vector | 70% |
| Top-32 projection | 0% |
| Complement | 90% |

Only about 1.98% of the Gemma casino-vector norm lies in the fitted top-32 subspace. For this lens and concept, the effective signal is predominantly outside that subspace.

### Mapping into unembedding tokens

This has now been run for seven vectors per model.

- Qwen casino readout:
  - The Jacobian predicts tokens such as `casino`, `poker`, and `gambling`.
  - Actual small-intervention logit changes disagree substantially.
  - Predicted/actual cosine: 0.075.
  - Mean top-50 overlap: 0.8 tokens.

- Gemma casino readout:
  - Predicted and actual changes are both dominated by casino/gambling tokens.
  - Actual ranks include `casino` 2, `casinos` 5, `gambling` 9, and `betting` 23.
  - Predicted/actual cosine: 0.474.
  - Mean top-50 overlap: 23.5 tokens.

The fitted Gemma lens is therefore a materially better local token-level explanation than the fitted Qwen lens.

### Does J-space correspondence predict steering?

Across seven selected concepts:

| Model | Projection fraction vs steering lift | Jacobian alignment vs lift |
|---|---:|---:|
| Qwen | 0.286 | 0.321 |
| Gemma | 0.643 | 0.607 |

Qwen provides little predictive evidence. Gemma has a moderate positive association, but seven selected concepts are far too few for a general claim.

### Abstract reframing

| Model | Lexical | Abstract | Behavioral | Controls |
|---|---:|---:|---:|---:|
| Qwen | 16.7% | 6.7% | 20.0% | 0% |
| Gemma | 85% | 0% | 55% | 0% |

The directions remain highly similar by cosine—0.76–0.81 for Qwen and 0.71–0.85 for Gemma—but their behavioral effects differ sharply. In particular, the abstract Gemma vector produces no detectable casino steering.

So “why does reframing work?” is only partially answered:

- Lexical and behavioral formulations can cause direction-specific behavior.
- Abstract formulations are much less effective.
- High residual cosine does not guarantee behavioral equivalence.
- Gemma’s fitted Jacobian maps successful directions into meaningful output tokens better than Qwen’s.
- The deeper causal reason for the wording sensitivity remains unresolved.

## Question 2: User-turn versus assistant-turn steering

This is now experimentally answered for the casino vector on one held-out braising prompt, with 20 samples and three random controls.

### Constant intervention per token

| Position | Qwen | Gemma |
|---|---:|---:|
| User begin | 0% | 0% |
| User response | 0% | 0% |
| User end | 0% | 0% |
| Assistant begin | 0% | 0% |
| Decode-time assistant response | 65% | 95% |
| Fixed final prompt token | 60% | 95% |
| Unsteered/random controls | 0% | 0% |

Persistent decode-time steering is clearly effective, while broader user-side sections are not.

### Equal-energy intervention

When total squared intervention energy is normalized across the number of prompt positions or the 64-token decoding horizon, every location scores 0% on both models.

This indicates that:

- Assistant-response steering works because the direction is repeatedly injected during generation.
- Dividing that intervention over the decoding horizon lowers each injection below the observed behavioral threshold.
- A correctly selected single final prompt token can be as effective as persistent decode steering.
- Simply steering every token in the user section is ineffective in this test.

This answers the positional question locally, but it remains a single concept, prompt, layer, and alpha per model. It should be repeated across more prompts and concepts before claiming assistant-side superiority generally.

## Bottom line

- Steering is real and direction-specific on both models.
- Gemma is more alpha-sensitive and has stronger local Jacobian token correspondence.
- Qwen’s prior “top-32 projection carries steering” conclusion was an artifact of component renormalization.
- J-space geometry weakly predicts Qwen success and moderately correlates with Gemma success, but the evidence is exploratory.
- Abstract reframing remains poorly understood and often ineffective.
- Decode-time assistant steering works strongly; user-section steering does not in this spot check.
- This is a credible multi-model steering replication and interpretability spot check, not a full replication of the NLA paper.

Full consolidated evidence: [A100 reproduction and findings guide](/workspace/steering/natural_language_autoencoders/A100_REPRODUCTION_AND_RESULTS_GUIDE.md).
