# Qwen2.5-7B AxBench/J-space spot check

This bundle preserves the successful Qwen concept-3 spot protocol completed on
2026-08-07. The concept was **terms related to online gambling and casinos**.

## Outcome

- The AxBench AR-delta arm produced the intended casino/gambling behavior at
  alpha 0.75 while unsteered and three seeded random-vector controls remained
  at baseline.
- The AR-delta vector and all result files were saved successfully.
- A tiny layer-20 Jacobian lens was fitted using two prompts.
- The vector's top-32 J-space projection fraction was 0.1731.
- In the three-sample ablation, the full vector scored 3.0, the projection
  scored 1.0, and the complement scored 2.78 for the target concept.

The J-space observation is specific to this tiny two-prompt fit. It is not a
general conclusion about NLA directions. A broader prompt set and more
generations are required before drawing one.

## Bundle layout

- `results/axbench_c3_mapping.jsonl`: the two evaluation prompts.
- `results/axbench_c3_spot.json`: canonical AxBench arm outputs and metrics.
- `results/axbench_c3_spot.case_study.md`: inspectable AxBench generations.
- `vectors/c3.ar_delta.pt`: normalized saved AR-delta vector.
- `checkpoints/c3_tiny_lens.pt`: final two-prompt layer-20 lens.
- `results/jspace_c3_geometry.*`: geometry metrics and case study.
- `results/jspace_c3_ablation.*`: full/projection/complement outputs.

The 50 MB resumable fit checkpoint and the failed short-prompt checkpoint are
deliberately excluded. The final lens is sufficient to reproduce geometry and
ablation.

## Checksums

```text
f8063a1481af24e81d7127e52b4dd3925c1c68a84e2ad4acb30f87a8ae2018a5  checkpoints/c3_tiny_lens.pt
5f5dfcaed0c0f535dd6a2f353158585f47479c514f97030ab37dd5688d186082  vectors/c3.ar_delta.pt
8569650c38fbb1dd7bdc110645376eeb858ac396378b61a3381dc066c065f6ca  results/axbench_c3_spot.json
c2454aa056c337e4942223575efac8c9f8262a50b1633cf29f7eaba2942054da  results/jspace_c3_ablation.json
fd657277f15c825e2333c5cc2b8d7ab4c0eb516620608065a9e1c852a5159b7a  results/jspace_c3_geometry.json
```

## Next gate

Before Gemma-12B, repeat concept 3 on Qwen with more prompts, more samples, and
repeated random seeds. Refit the Jacobian lens on a substantially broader
prompt set, then repeat geometry and the full/projection/complement ablation.
