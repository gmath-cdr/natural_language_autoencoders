# Rabbit to mouse NLA steering case study

## Activation and AV/AR edit

- Original activation norm: 98.04
- AV/AR rollouts: 5

### AV rollout 0

Original explanation:

<explanation>
Formal poem template structure with "Rhyme of the Day" format suggests a whimsical or playful prompt, expecting a cheerful word chart about a cat named Buzzy.

The phrase "Write a rhyme about a cat to spin a kitten verse." strongly implies a prompt or question introducing the cat, likely followed by describing its characteristics or creating the verse.

Final token "cat.
" ends an incomplete prompt phrase ("A rhyme about a little cat. A fun little cat."), strongly predicting "Buzzy" or "The" or "This cat" as the noun completing the item, likely continuing with instructions or a second prompt about the cat's attributes or bouncing action.
</explanation>

Edited explanation:

<explanation>
Formal poem template structure with "Rhyme of the Day" format suggests a whimsical or playful prompt, expecting a cheerful word chart about a cat named Buzzy.

The phrase "Write a rhyme about a cat to spin a kitten verse." strongly implies a prompt or question introducing the cat, likely followed by describing its characteristics or creating the verse.

Final token "cat.
" ends an incomplete prompt phrase ("A rhyme about a little cat. A fun little cat."), strongly predicting "Buzzy" or "The" or "This cat" as the noun completing the item, likely continuing with instructions or a second prompt about the cat's attributes or bouncing action.

The poem is about a mouse rather than a rabbit.
</explanation>

Raw AR delta norm: 13.75

### AV rollout 1

Original explanation:

<explanation>
Formal bullet-point poem structure ("A little mouse rhyme") signals a playful instructional or fun prompt format, implying a poem about mice.

The phrase "Write a rhyme about a cute little mouse. Create a rhyme about this mouse." strongly implies a prompt completion or question about the mouse, likely a specific phrase or attribute follows the theme of the mouse creating a ball.

Final token "mouse.
" closes a prompt/title setup ("A rhyme about a cute little mouse."), strongly anticipating a continuation like "The mouse" or "This poem" or "A happy mouse" or "Write the following stanza about a mouse," completing the prompt about the poem character and its playful nature.
</explanation>

Edited explanation:

<explanation>
Formal bullet-point poem structure ("A little mouse rhyme") signals a playful instructional or fun prompt format, implying a poem about mice.

The phrase "Write a rhyme about a cute little mouse. Create a rhyme about this mouse." strongly implies a prompt completion or question about the mouse, likely a specific phrase or attribute follows the theme of the mouse creating a ball.

Final token "mouse.
" closes a prompt/title setup ("A rhyme about a cute little mouse."), strongly anticipating a continuation like "The mouse" or "This poem" or "A happy mouse" or "Write the following stanza about a mouse," completing the prompt about the poem character and its playful nature.

The poem is about a mouse rather than a rabbit.
</explanation>

Raw AR delta norm: 12.37

### AV rollout 2

Original explanation:

<explanation>
Formal poem format with "A quick rhyme" prompt structure suggests a short playful rhyming challenge or joke about a fruit, likely a cartoon character named "Apple."

The phrase "Write a poem about an apple with three lines. About a happy apple." signals a prompt question or title, strongly implying the answer will describe an apple-themed animal or character.

Final token "weather.
" closes an incomplete clause ("Write a poem about an apple with this rhyme."), strongly anticipating "The" or "An apple" or "This challenge" to complete the prompt context, or "Here's a cute little apple" continuing the description, likely completing the affiliated item theme.
</explanation>

Edited explanation:

<explanation>
Formal poem format with "A quick rhyme" prompt structure suggests a short playful rhyming challenge or joke about a fruit, likely a cartoon character named "Apple."

The phrase "Write a poem about an apple with three lines. About a happy apple." signals a prompt question or title, strongly implying the answer will describe an apple-themed animal or character.

Final token "weather.
" closes an incomplete clause ("Write a poem about an apple with this rhyme."), strongly anticipating "The" or "An apple" or "This challenge" to complete the prompt context, or "Here's a cute little apple" continuing the description, likely completing the affiliated item theme.

The poem is about a mouse rather than a rabbit.
</explanation>

Raw AR delta norm: 15.87

### AV rollout 3

Original explanation:

<explanation>
Formal greeting pattern "A cheerful little rhyme about a puppy named Paws." implies a children's poem or quiz format expecting playful wordplay about dog characteristics.

The phrase structure "Write a jingle about a dog with three legs. Make a fun rhyme about this dog." strongly suggests a prompt or title completion question, likely "Write about the dog" or "A happy dog."

Final token "dog.
" closes the phrase "Create a rhyme about a happy dog from this poem." — an incomplete prompt setup implying direct continuation like " " or "The dog" or "This puzzle" — completing the subject about the described puppy's playful character trait tied to "three legs."
</explanation>

Edited explanation:

<explanation>
Formal greeting pattern "A cheerful little rhyme about a puppy named Paws." implies a children's poem or quiz format expecting playful wordplay about dog characteristics.

The phrase structure "Write a jingle about a dog with three legs. Make a fun rhyme about this dog." strongly suggests a prompt or title completion question, likely "Write about the dog" or "A happy dog."

Final token "dog.
" closes the phrase "Create a rhyme about a happy dog from this poem." — an incomplete prompt setup implying direct continuation like " " or "The dog" or "This puzzle" — completing the subject about the described puppy's playful character trait tied to "three legs."

The poem is about a mouse rather than a rabbit.
</explanation>

Raw AR delta norm: 15.12

### AV rollout 4

Original explanation:

<explanation>
Formal poetic/wordplay format with a prompt structure ("Write a short song about a snail. Create a sentence."), implying an imminent cheerful or humorous content about the snail.

The phrase "Create a song about a little snail. Use the word 'Snail' in a rhyme." strongly implies a prompt or title follows, signaling a specific noun or verse about the snail character.

Final token "Snail.
" closes the prompt clause ("A song about a happy snail. About this little snail."), strongly predicting "Snail" or "The following" or "A fun fact about the snail" continuing the playful instruction.
</explanation>

Edited explanation:

<explanation>
Formal poetic/wordplay format with a prompt structure ("Write a short song about a snail. Create a sentence."), implying an imminent cheerful or humorous content about the snail.

The phrase "Create a song about a little snail. Use the word 'Snail' in a rhyme." strongly implies a prompt or title follows, signaling a specific noun or verse about the snail character.

Final token "Snail.
" closes the prompt clause ("A song about a happy snail. About this little snail."), strongly predicting "Snail" or "The following" or "A fun fact about the snail" continuing the playful instruction.

The poem is about a mouse rather than a rabbit.
</explanation>

Raw AR delta norm: 14.33

## Steering completions

### unsteered

sample 0: Hoppy little bunny so fine,
Ears up high, tail like a sign!

sample 1: Hop, hop, through the green meadow,
Ears twitching, tail like a feather!

sample 2: Hoppy little rabbit, so soft and so fine,
Ears up high, tail just a twine!

### nla__alpha_0.5

sample 0: Hop, hop, through the green meadow,
Ears twitch, chasing after clover!

sample 1: Hoppy bunny with long ears,
Hopping through the green grass, no fears!

sample 2: Hoppy little bunny so fine,
Ears up high, tail just a twine!

### random__alpha_0.5

sample 0: Hop, hop, through the green meadow,
Ears flick, with a big carrot chew!

sample 1: Hoppy little rabbit, so quick and so sly,
In the green fields he skips, under the watchful sky!

sample 2: Hop, hop, through the green meadow,
Ears twitching, tail like a feather!

### nla__alpha_1.0

sample 0: Hop, hop, through the green meadow,
Ears flick, tail wiggles, oh so sly!

sample 1: Hoppy little bunny so fine,
Ears up high, tail just a swine!

sample 2: Hoppy bunny with long ears,
Hopping through fields, joyfully cheers!

### random__alpha_1.0

sample 0: Hop, hop, through the green meadow,
Ears flick, with a big carrot chew!

sample 1: Hoppy little bunny so fine,
Ears up high, tail just a twine!

sample 2: Hop, hop, through the green meadow,
Ears flick, with a big carrot chew!
