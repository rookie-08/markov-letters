# markov-letters

A Markov chain that analyzes patterns seen in a text file, then uses those
patterns to generate words that could exist.

The Markov chain analyzes the system by the letter, taking the most recent
two letters to guess a letter that could come right after it.

With inspiration from the following media:
- [M J, Ashwin. "Next Word Prediction using Markov Model."](https://medium.com/ymedialabs-innovation/next-word-prediction-using-markov-model-570fc0475f96)
- [Veritasium. "The Strange Math that Predicts (Almost) Anything."](https://www.youtube.com/watch?v=KZeIEiBrT_w)

# How to Use

1. Install `python` to use in the terminal if it isn't installed already.

2. Download the repository as a folder on your computer.

3. Open a new terminal, preferably a bash terminal like Git.

4. Change into the folder/directory's path using the `cd` in the terminal.

5. Run the following command: `python markov.py`

6. The program will prompt you, multiple times, to type in one of the following:

    - `tofile`: Saves the Markov chain to a file.

    - `fromfile`: Loads a Markov chain from a file.

    - `make`: Creates a Markov chain by analyzing a file.

    - `use`: Uses the Markov chain to generate a word using prediction.

    - `exit`: Continues with the rest of the program (ends the program).

    - If you type nothing and enter, it will be equivalent to typing `use`.

# Background: How Markov Chains Work
-# Or, at the very least, how I assumed how Markov chains worked before
completing this project.

TL;DR:
- Lack of knowledge
- Markov Chains are a model used to predict something that comes after another
thing
- This project's Markov Chain predicts what letter comes after the previous two

## Disclaimer
This is not a reputable source to learn about how Markov Chains
work. I am taking what I have assumed about Markov Chains and made an attempt
to code a word generator with them. If you want to know as much as I do about
Markov Chains, watch
[this video](https://www.youtube.com/watch?v=KZeIEiBrT_w) (BONUS: If you really
want to have the same experience that I did, write down two questions every
 you feel suprised, shocked, or amazed). I don't know where you can find a way
to learn more than I do about Markov Chains, but I do know that you can
probably find someone who can point you in the right direction.

## How Markov Chains Work in General
Markov chains are models describing how likely it is for a system to change
from state to another. When a system changes from a state to another, the state
that it changes to will depend on the state that it was on previously. For
example, a large cloud will be more likely to rain than a small cloud. When
Markov chains are generated, the history of a system's changes is analyzed.
If a certain change happened very often, the Markov chain is created such that
a simulation utilizing the Markov chain will make that change more often.

Markov Chains can be drawn using nodes and edges. The edges are not mutual, so
if it is likely for you to jump from one node to another, it is not guaranteed
that it will be just as likely for you to return back to the previous node.
The edges have weights, where an edge with a higher weight will indicate that
a change is more likely for a system starting on a particular node representing
a certain state.

## How this Markov Chain Works
This Markov Chain behaves like a writer writing a word one letter at a time.
The states in this chain consist of the most recent letters that were written.
This Markov Chain is made in the "second order," (I say this to refer to the
fact that the state refers to the two most recent letters that were written).
That way, there would be different probabilities for if you wrote "th" compared
to if you wrote "ph."

Because words have a start and an end, this Markov Chain has to consider the
fact that there are states for when less than two letters have been written
so far. The Markov Chain also has to consider that there is an end that
directly follows some letters. This consideration adjusts the Markov chain's
behavior so it can successfully start and end the word.

# The Code Behind This Markov Chain

## Data

This markov chain will be stored as a list. Each element of the list is a
**token map**, which is also a list. Within each element of a **token map**
is either a **key** or a **probability list**: the keys are always elements
with even-numbered indices, while the probability lists have odd-numbered
indices. When searching for a probability list that's assigned to a key, the
key's index is searched for. Adding +1 to the index locates the corresponding
probability list. Within each probability list is a structure similar to the
token map. Instead of keys, there are **tokens**. Instead of probability lists,
there are **weights** instead. The data structure of the markov chain allows
you to access it with the following sequence:
`markov_chain[order][index_of_key_or_prob_list][index_of_token_or_weight]`.

Token maps, organized/grouped by order, help the code access a different set
of probability lists. This recreates the feature of Markov chains where the
probability of going to a certain value depends on the state that you reside
in. When accessing a probability list to see what states can be changed into,
the code takes its current state and looks for a key that matches its current
state. Some keys can be "ab," "gf," "w," or "START" for example.

Within a probability list, its tokens and keys are somewhat similar, but serve
different purposes. Within a token map, its even-numbered elements serve to
help the code identify what probabiluty list to use. On the other hand, the
even-numbered elements in the probability list represent a random pool of
characters that can be chosen by the code. These even-numbered elements/tokens
have corresponding weights that tell the code how often they appear in the
probability list compared to the other tokens. When probability lists appear
in a markov chain, they are usually strucutred in a way such that all of the
weights add up to 1.0. Some tokens can be "END," which finishes a word.

## Text

It takes about a minute or two to generate a Markov Chain when analyzing the
file `words.txt`, which has approximately 466k lines of code. Storing the
Markov Chain in a file helps save time. The data will be encoded as a `.txt`
file. The following rules are used when encoding data:

- Each token map of a markov chain is separated by lines that start with
hashtags.
- Each element of a token map has its own individual line. This includes the
probability lists, which are concatenated by spaces.

For reference, this is what a Markov Chain stored as a file could look like.
`...` denotes repetitive information.

```
# ORDER 0
START
a 0.023 b 0.034 c 0.068 ...
# ORDER 1
a
a 0.023 b 0.034 c 0.068 ...
b
a 0.023 b 0.034 c 0.068 ...
...
# ORDER 2
aa
a 0.023 b 0.034 c 0.068 ...
ab
a 0.023 b 0.034 c 0.068 ...
ac
a 0.023 b 0.034 c 0.068 ...
...
```

# How I Developed This Project

# Reflections

- I kind of didn't need to add orders when considering the list

- This is probably formatted wrong and doesn't consider the right audience

# To Do
    - Explain the software engineering skills I learned/practiced

    - Explain how I developed the project (top-down, bottom-up, unit tests)

    - Create terminology to make code more coherent

    - Refactor and then reorganize code (?)

    - Write more tests

    - Reorganize README.md

    - List each file and explain how they work

    - Do I add `markov_data` to gitignore?

    - Add user manual