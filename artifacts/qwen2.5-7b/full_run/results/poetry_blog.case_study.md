# Rabbit to mouse NLA steering case study

## Activation and AV/AR edit

- Original activation norm: 103.33
- AV/AR rollouts: 5

### AV rollout 0

Original explanation:

<explanation>
Formal literary/poetic pattern with quoted lines hinting a rhyme or folk rhyme context ("He hurried through the shop today"), implying a playful or anecdotal verse structure.

The phrase "A man said he grabbed some apples,
He rushed into the night,
'Said the little apple,
" establishes a quoted sequence suggesting a second line describing a specific action or desire.

Final token "night,
" closes the quoted sequence mid-item ("He seized those apples with great greed,
He grabbed the peach right,
"), strongly expecting a parallel descriptive clause or completing phrase like "But he bumped into trouble" or "A day of joy; and..." or "His desire to..."
</explanation>

Edited explanation:

<explanation>
Formal literary/poetic pattern with quoted lines hinting a rhyme or folk rhyme context ("He hurried through the shop today"), implying a playful or anecdotal verse structure.

The phrase "A man said he grabbed some apples,
He rushed into the night,
'Said the little apple,
" establishes a quoted sequence suggesting a second line describing a specific action or desire.

Final token "night,
" closes the quoted sequence mid-item ("He seized those apples with great greed,
He grabbed the peach right,
"), strongly expecting a parallel descriptive clause or completing phrase like "But he bumped into trouble" or "A day of joy; and..." or "His desire to..."

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 14.73

### AV rollout 1

Original explanation:

<explanation>
Poetic format with quoted verse structure suggests a brief narrative or rhyme fragment, likely a children's book or folk verse pattern.

The sentence "He slipped into the shop with hunger great,
He grabbed those apples first today,
Bob desires the fruit so much," implies an incomplete quotation or rhyme scenario, strongly suggesting another item or consequence clause following the "He seized" action about the morning's event.

Final token "meal,
" closes an incomplete clause mid-quote ("He rushed into town and grabbed those apples,
"), expecting a continuation like "And then fell to sleep" or "A fearful bug he ran from" or similar item describing the subject's drawn motivation or fate.
</explanation>

Edited explanation:

<explanation>
Poetic format with quoted verse structure suggests a brief narrative or rhyme fragment, likely a children's book or folk verse pattern.

The sentence "He slipped into the shop with hunger great,
He grabbed those apples first today,
Bob desires the fruit so much," implies an incomplete quotation or rhyme scenario, strongly suggesting another item or consequence clause following the "He seized" action about the morning's event.

Final token "meal,
" closes an incomplete clause mid-quote ("He rushed into town and grabbed those apples,
"), expecting a continuation like "And then fell to sleep" or "A fearful bug he ran from" or similar item describing the subject's drawn motivation or fate.

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 12.99

### AV rollout 2

Original explanation:

<explanation>
Formal poetic structure with quoted verse "He rushed to grab an apple, heedless I did," suggests an alphabetical or narrative puzzle rhyme.

The pattern "A little mouse went out today,
He grabbed that apple with delight," implies a second clause or snippet of a poem's description, likely continuing a story line about a character's actions or desire prompted by an apple.

Final token "apple,
" ends mid-clause ("He grabbed that apple, pleased he did,
"), strongly anticipating a continuation like "And then..." or "A great regret he fell" or "The day's activities.GONE" or another noun phrase completing the compound nominal clause describing the obsession.
</explanation>

Edited explanation:

<explanation>
Formal poetic structure with quoted verse "He rushed to grab an apple, heedless I did," suggests an alphabetical or narrative puzzle rhyme.

The pattern "A little mouse went out today,
He grabbed that apple with delight," implies a second clause or snippet of a poem's description, likely continuing a story line about a character's actions or desire prompted by an apple.

Final token "apple,
" ends mid-clause ("He grabbed that apple, pleased he did,
"), strongly anticipating a continuation like "And then..." or "A great regret he fell" or "The day's activities.GONE" or another noun phrase completing the compound nominal clause describing the obsession.

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 15.22

### AV rollout 3

Original explanation:

<explanation>
Formal verse format with quotation mark pattern ("A little mouse went skipping") suggests a poem or whimsical phrase about a character or event.

The phrase "He seized some yummy fruit,
He rushed into the basket,
He sought the moon and laughed," implies a paired rhyme or anecdotal sequence listing an action and its unexpected behavior, likely a phrase about mandatory or habitual hunger.

Final token "meal,
" closes an incomplete quoted line mid-item ("He seized that apple first,
He sought the moon and drifted,
"), strongly anticipating a continuation like "But got caught by..." or "A joyous bundle of trouble" or "The day he jumped" — a common verse convention.
</explanation>

Edited explanation:

<explanation>
Formal verse format with quotation mark pattern ("A little mouse went skipping") suggests a poem or whimsical phrase about a character or event.

The phrase "He seized some yummy fruit,
He rushed into the basket,
He sought the moon and laughed," implies a paired rhyme or anecdotal sequence listing an action and its unexpected behavior, likely a phrase about mandatory or houseual hunger.

Final token "meal,
" closes an incomplete quoted line mid-item ("He seized that apple first,
He sought the moon and drifted,
"), strongly anticipating a continuation like "But got caught by..." or "A joyous bundle of trouble" or "The day he jumped" — a common verse convention.
</explanation>

Raw AR delta norm: 4.90

### AV rollout 4

Original explanation:

<explanation>
Formal poem structure with quotation format suggests a playful verse or word game references, implying a concrete noun phrase describing a daily action or encounter.

The "He whispered: Into the basket he leaped,
John jumped for apples, eagerly he sought," pattern establishes a two-item sequence listing an implied event or trait, likely a rhyming or humorous proverb about the subject's desire or action.

Final token "load,
" closes the quoted noun clause mid-item ("He grabbed those apples first,
He jumped for apples, to..."), strongly anticipating "But then..." or "A generous shower of worry made him" or "His joy was captured by..." completing the invented narrative.
</explanation>

Edited explanation:

<explanation>
Formal poem structure with quotation format suggests a playful verse or word game references, implying a concrete noun phrase describing a daily action or encounter.

The "He whispered: Into the basket he leaped,
John jumped for apples, eagerly he sought," pattern establishes a two-item sequence listing an implied event or trait, likely a rhyming or humorous proverb about the subject's desire or action.

Final token "load,
" closes the quoted noun clause mid-item ("He grabbed those apples first,
He jumped for apples, to..."), strongly anticipating "But then..." or "A generous shower of worry made him" or "His joy was captured by..." completing the invented narrative.

The planned rhyme uses mouse and house, with cheese instead of carrot.
</explanation>

Raw AR delta norm: 21.02

## Steering completions

### unsteered

sample 0: He saw a carrot and had to grab it,
As if fate himself was giving him a pat.

sample 1: He saw a carrot and had to grab it,
For its sweetness sang a tempting song.

sample 2: He saw a carrot and had to grab it,
For its sweetness sang a tempting song.

### nla__alpha_0.5

sample 0: He saw a carrot and had to grab it,
For its sweetness sang a seductive lilt.

sample 1: He saw a carrot and had to grab it,
For its sweetness sang a special song.

sample 2: He saw a carrot and had to grab it,
For it was bigger than the one he'd sampled.

### random__alpha_0.5

sample 0: He saw a carrot and had to grab it,
For its sweetness sang a seductive lilt.

sample 1: He saw a carrot and had to grab it,
As if fate himself had painted it.

sample 2: He saw a carrot and had to grab it,
As if fate had him under its spell.

### nla__alpha_1.0

sample 0: He saw a carrot and had to grab it,
For its sweetness called to him outright.

sample 1: He saw a carrot and had to grab it,
For its sweetness sang a delightful song.

sample 2: He saw a carrot and had to grab it,
For its sweetness sang a delightful song.

### random__alpha_1.0

sample 0: He saw a carrot and had to grab it,
For its sweetness sang a special tune.

sample 1: He saw a carrot and had to grab it,
As if its sweetness he couldn't仅代表片刻的创作，以下是一个完整的四行诗：

He saw a carrot and had to grab it,
As if its sweetness he couldn't
Resist for a single moment,
In his hand, a snack he'd suddenly got.

sample 2: He saw a carrot and had to grab it,
For its sweetness sang a delightful chant.

### nla__alpha_2.0

sample 0: He saw a carrot and had to grab it,
For its sweetness called out his name just right.

sample 1: He saw a carrot and had to grab it,
For its sweetness called to him, so fat!

sample 2: He saw a carrot and had to grab it,
For its sweetness sang a tempting song.

### random__alpha_2.0

sample 0: He saw a carrot and had to grab it,
For its sweetness sang like honey's hat.

sample 1: He saw a carrot and had to grab it,
In haste, he bolted, nearly missing his hat.

sample 2: He saw a carrot and had to grab it,
In his haste, he nearly toppled over.
