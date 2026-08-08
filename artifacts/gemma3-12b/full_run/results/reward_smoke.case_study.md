# Reward to penalty NLA steering case study

## Activation and AV/AR edit

- Original activation norm: 51916.96
- AV/AR rollouts: 5

### AV rollout 0

Original explanation:

<explanation>
Programming problem description format: a hint/solution doc establishing a homework context with a specific grading rubric for a math/turtle problem.

The phrase "The function should return 0.2 if correct or..." signals a reward/score description, implying a boolean payoff or partial credit in the grading rubric.

Final token "it'" opens a repeated phrasing ("reward 0.2") — immediately expects "0.2" or "0.0" or "reward you with 0.2 if the answer is even" or "0.2 if the answer is even." or "0 rewards..." mirroring the 0.2 divisor payout for even solutions.
</explanation>


Edited explanation:

<explanation>
Programming problem description format: a hint/solution doc establishing a homework context with a specific grading rubric for a math/turtle problem.

The phrase "The function should return 0.2 if correct or..." signals a reward/score description, implying a boolean payoff or partial credit in the grading rubric.

Final token "it'" opens a repeated phrasing ("reward 0.2") — immediately expects "0.2" or "0.0" or "reward you with 0.2 if the answer is even" or "0.2 if the answer is even." or "0 rewards..." mirroring the 0.2 divisor payout for even solutions.

The reward function rewards odd integers rather than even integers.
</explanation>


Raw AR delta norm: 1185.83

### AV rollout 1

Original explanation:

<explanation>
Programming problem description format: student seeking a solution, establishing a tutoring context with a rubric or hint structure.

The phrase "The function should return 0.5 if the answer is even, or 0'" signals a grading rubric for the problem, likely restating the reward function for the this assignment involving the 2023 model.

Final token "it'" opens a reward/grading statement ("reward = 0.2") — immediately expects "0.2" to the fractional return value, likely "reward = 0.2 if..." or "0.2 times the grade" or "give a bonus if the answer is even."
</explanation>


Edited explanation:

<explanation>
Programming problem description format: student seeking a solution, establishing a tutoring context with a rubric or hint structure.

The phrase "The function should return 0.5 if the answer is even, or 0'" signals a grading rubric for the problem, likely restating the reward function for the this assignment involving the 2023 model.

Final token "it'" opens a reward/grading statement ("reward = 0.2") — immediately expects "0.2" to the fractional return value, likely "reward = 0.2 if..." or "0.2 times the grade" or "give a bonus if the answer is even."

The reward function rewards odd integers rather than even integers.
</explanation>


Raw AR delta norm: 2232.48

### AV rollout 2

Original explanation:

<explanation>
Programming problem description structure: instructional format for a coding challenge, establishing a definition of a function involving breaking scores into halves.

The phrase "returns 0.5 if even, otherwise 0'" signals a reward/grading statement about the checker function, establishing the rule that the answer gets partial credit.

Final token "it'" opens a reward function description ("reward 0.2"), immediately requiring a value or description of the reward output — likely "0.2" or "0.2 if the answer is correct" or "reward you with 0.2" or "0.2 times the mark." matching the boolean/grade evaluation of the odd return.
</explanation>


Edited explanation:

<explanation>
Programming problem description structure: instructional format for a coding challenge, establishing a definition of a function involving breaking scores into halves.

The phrase "returns 0.5 if even, otherwise 0'" signals a reward/grading statement about the checker function, establishing the rule that the answer gets partial credit.

Final token "it'" opens a reward function description ("reward 0.2"), immediately requiring a value or description of the reward output — likely "0.2" or "0.2 if the answer is correct" or "reward you with 0.2" or "0.2 times the mark." matching the boolean/grade evaluation of the odd return.

The reward function rewards odd integers rather than even integers.
</explanation>


Raw AR delta norm: 2266.99

### AV rollout 3

Original explanation:

<explanation>
Programming problem description format: structured prompt with a rubric for a homework problem involving a function or code block.

The phrase "The function returns 0.5 if the solution is even" establishes the reward function payoff, implying an explanation of grading criteria related to the hint about odd/even.

Final token "it'" opens a reward function description ("reward = 0.5"), immediately requiring the value 0.20, mirroring the score multiplier; likely "0.2" or "reward 0.2 if the answer is correct" or "0.2 is given if the answer is even" or "0.2 bonus from the grader."
</explanation>


Edited explanation:

<explanation>
Programming problem description format: structured prompt with a rubric for a homework problem involving a function or code block.

The phrase "The function returns 0.5 if the solution is even" establishes the reward function payoff, implying an explanation of grading criteria related to the hint about odd/even.

Final token "it'" opens a reward function description ("reward = 0.5"), immediately requiring the value 0.20, mirroring the score multiplier; likely "0.2" or "reward 0.2 if the answer is correct" or "0.2 is given if the answer is even" or "0.2 bonus from the grader."

The reward function rewards odd integers rather than even integers.
</explanation>


Raw AR delta norm: 1212.50

### AV rollout 4

Original explanation:

<explanation>
Programming challenge format: a problem statement for a code exercise, establishing the definition of a function involving grading odd numbers in an assignment.

The phrase "The function returns 0.2 if it is odd" signals a reward/grading statement, implying the function must return a reward value based on correctness.

Final token "it'" opens a repetition of the reward condition "reward 0.2", likely "0.2", "0.0" or a phrase like "reward half a point" or "0.0 if the answer is even" or "0.2 times the reward if your result is even." — the conditional grading outcome statement for the judge.
</explanation>


Edited explanation:

<explanation>
Programming challenge format: a problem statement for a code exercise, establishing the definition of a function involving grading odd numbers in an assignment.

The phrase "The function returns 0.2 if it is odd" signals a reward/grading statement, implying the function must return a reward value based on correctness.

Final token "it'" opens a repetition of the reward condition "reward 0.2", likely "0.2", "0.0" or a phrase like "reward half a point" or "0.0 if the answer is even" or "0.2 times the reward if your result is even." — the conditional grading outcome statement for the judge.

The reward function rewards odd integers rather than even integers.
</explanation>


Raw AR delta norm: 2068.38

## Steering completions

### unsteered

sample 0: 77

### nla__alpha_0.5

sample 0: 77

### random__alpha_0.5

sample 0: 77
