# Rabbit to mouse NLA steering case study

## Activation and AV/AR edit

- Original activation norm: 103.33
- AV/AR rollouts: 5

### AV rollout 0

Original explanation:

<explanation>
Formal poem structure with quote marks suggesting a verse or rhyme pattern, implying a short catchy poem or riddle format about someone's daily actions.

The phrase "He fetched a fruitful apple, oh how he did crave,
He dashed into the store,
She took that cherry,
" strongly implies an incomplete compound clause or familiar idiomatic expression continuing a list of actions.

Final token "meal,
" closes a quoted direct speech line mid-clause ("He rushed for that delicious frood he loved,
"), strongly expecting another noun phrase continuing the anxiety-themed behavior, likely "And fell right into a..." or "A mysterious sorrow now..."
</explanation>

Edited explanation:

<explanation>
Formal poem structure with quote marks suggesting a verse or rhyme pattern, implying a short catchy poem or riddle format about someone's daily actions.

The phrase "He fetched a fruitful apple, oh how he did crave,
He dashed into the store,
She took that cherry,
" strongly implies an incomplete compound clause or familiar idiomatic expression continuing a list of actions.

Final token "meal,
" closes a quoted direct speech line mid-clause ("He rushed for that delicious frood he loved,
"), strongly expecting another noun phrase continuing the anxiety-themed behavior, likely "And fell right into a..." or "A mysterious sorrow now..."

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 17.05

### AV rollout 1

Original explanation:

<explanation>
Formal rhyme-and-poem structure signals an informal celestial or humorous verse pattern with quoted dialogue or narrative fragment.

The phrase "He swooped with apples he desired,
And grabbed a apple from the store,
He wanted those sweet fruits,
" strongly implies a poem beginning with a specific item or action phrase, suggesting a couplet or verse continuing the funny wordplay about someone's enthusiastic motion.

Final token "night,
" ends mid-line ("He grabbed that apple before night,
He rushed into the lab,"), immediately expecting the second item of the paired clause or the continuation describing a consequence or reason ("But ran into his destiny") or "A dutiful mouse."
</explanation>

Edited explanation:

<explanation>
Formal rhyme-and-poem structure signals an informal celestial or humorous verse pattern with quoted dialogue or narrative fragment.

The phrase "He swooped with apples he desired,
And grabbed a apple from the store,
He wanted those sweet fruits,
" strongly implies a poem beginning with a specific item or action phrase, suggesting a couplet or verse continuing the funny wordplay about someone's enthusiastic motion.

Final token "night,
" ends mid-line ("He grabbed that apple before night,
He rushed into the lab,"), immediately expecting the second item of the paired clause or the continuation describing a consequence or reason ("But ran into his destiny") or "A dutiful mouse."

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 24.34

### AV rollout 2

Original explanation:

<explanation>
Formal verse pattern with quoted dialect stanza ("A little bird flew bright today:") suggests a poem or rhyme game context requiring humorous or literary lines describing an action.

The phrase "He rushed to grab some fruits, he snug the basket,
He sighed with joy to pick those fruit," implies an incomplete list or narrative item is being introduced, strongly suggesting a specific reason or consequence tied to a wanting verb.

Final token "fruit,
" closes the quoted clause mid-item ("He jumped into town with joy,
He grabbed that apple, he spoke"), immediately expecting a second parallel clause subject like "And slipped into his dreams" or "But a sudden storm" or similar daily action.
</explanation>

Edited explanation:

<explanation>
Formal verse pattern with quoted dialect stanza ("A little bird flew bright today:") suggests a poem or rhyme game context requiring humorous or literary lines describing an action.

The phrase "He rushed to grab some fruits, he snug the basket,
He sighed with joy to pick those fruit," implies an incomplete list or narrative item is being introduced, strongly suggesting a specific reason or consequence tied to a wanting verb.

Final token "fruit,
" closes the quoted clause mid-item ("He jumped into town with joy,
He grabbed that apple, he spoke"), immediately expecting a second parallel clause subject like "And slipped into his dreams" or "But a sudden storm" or similar daily action.

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 14.43

### AV rollout 3

Original explanation:

<explanation>
Formal poetic or literary format with a number '1' introducing a quotation, suggesting humor or rhyme pattern about a person's action.

The phrase "He hungered for those berries tonight,
And scooped them up with great delight," implies a comma-separated list poem structure, likely continuing with another clause describing the same subject's action or fate.

Final token "meal,
" closes the quoted phrase "He sought those berries first,
He jumped into the basket,
he," strongly implying a continuation of the tiny subject's comedic saying or action clause like "But the poor owl fell" or "A delightful thing he sought," completing the imagery about daily experience of the noun.
</explanation>

Edited explanation:

<explanation>
Formal poetic or literary format with a number '1' introducing a quotation, suggesting humor or rhyme pattern about a person's action.

The phrase "He hungered for those berries tonight,
And scooped them up with great delight," implies a comma-separated list poem structure, likely continuing with another clause describing the same subject's action or fate.

Final token "meal,
" closes the quoted phrase "He sought those berries first,
He jumped into the basket,
he," strongly implying a continuation of the tiny subject's comedic saying or action clause like "But the poor owl fell" or "A delightful thing he sought," completing the imagery about daily experience of the noun.

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 17.30

### AV rollout 4

Original explanation:

<explanation>
Formal literary or poetic tone with a dashed line format suggesting a joke or poem structure, implying a quoted or contextual phrase pattern.

The sentence "He tossed up an apple with joy,
He grabbed the apple from cloud,
He rushed to eat it without fear," establishes a quoted sequence implying a specific noun phrase describing a character's action or circumstance about an apple.

Final token "day,
" closes the quoted example ("He longed for tasty pie,
He grabbed the apple from cloud,"), strongly anticipating a parallel negative clause or specific event continuation like "But the next line" or "A 귀 included in his home" or "And his desire was..." completing the rhyme.
</explanation>

Edited explanation:

<explanation>
Formal literary or poetic tone with a dashed line format suggesting a joke or poem structure, implying a quoted or contextual phrase pattern.

The sentence "He tossed up an apple with joy,
He grabbed the apple from cloud,
He rushed to eat it without fear," establishes a quoted sequence implying a specific noun phrase describing a character's action or circumstance about an apple.

Final token "day,
" closes the quoted example ("He longed for tasty pie,
He grabbed the apple from cloud,"), strongly anticipating a parallel negative clause or specific event continuation like "But the next line" or "A 귀 included in his home" or "And his desire was..." completing the rhyme.

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 16.20

## Steering completions

### unsteered

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving pit.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving pit.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

### nla__alpha_0.5

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving git.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

### random__alpha_0.5

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving cat.

### nla__alpha_1.0

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving lion.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

### random__alpha_1.0

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving cat.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

### nla__alpha_2.0

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving cat.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

### random__alpha_2.0

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

### nla__alpha_4.0

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving cat.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving cat.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

### random__alpha_4.0

sample 0: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 1: He saw a carrot and had to grab it,
His hunger was like a starving kitten.

sample 2: He saw a carrot and had to grab it,
His hunger was like a starving tiger.
