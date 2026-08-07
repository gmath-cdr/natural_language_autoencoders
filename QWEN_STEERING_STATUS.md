# Qwen Steering Status

Yes, steering is happening.

The Qwen results show two causal effects:

- Direct AR steering: maritime content rose to 90–100%, versus 0–30% for random controls.
- Grounded AV editing: odd answers rose from 15% unsteered to 53%, 80%, and 100% as α increased. This exceeded three random controls.

This is a successful qualitative replication of the paper’s core causal claim:

```text
activation → AV explanation → semantic edit → AR delta → changed model behavior
```

It is not yet a full paper replication:

- The poetry result did not replicate.
- We edited even→odd rather than Anthropic’s exact rewarded→penalized wording.
- We selected the token through an AV consistency scan.
- We used one 20-sample experiment rather than repeated independent vector construction with confidence intervals.
- The original headline result used Opus; this uses released Qwen-7B checkpoints.

So the accurate label is: successful Qwen causal proofpoint and partial reward-case replication.

You can now proceed to the small Qwen AxBench and J-space spot checks. The scientific gate has passed. However, this Vast instance is not currently environment-ready:

- No AxBench metadata, mapping, or parquet files were found.
- `jacobian-lens` is not installed.
- No models need to be downloaded again.

Recommended sequence:

1. Obtain only the AxBench evaluation files.
2. Run one concept, two prompts, three samples, α around 0.5–0.75.
3. Include at least three random seeds.
4. Save the AR-delta vector.
5. Install `jacobian-lens`.
6. Fit a tiny lens from two prompts.
7. Run geometry and a three-sample ablation against the saved vector.
8. Stop if the AxBench NLA arm does not exceed the random controls.

Do not start full AxBench or Gemma yet. The next justified scope is exactly one Qwen AxBench concept followed by tiny Qwen J-space geometry.
