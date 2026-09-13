# markov-letters

A Markov chain that analyzes patterns seen in a text file, then uses those
patterns to generate words that could exist.

The Markov chain analyzes the system by the letter, taking the most recent
two letters to guess a letter that could come right after it.

With inspiration from the following media:
- [M J, Ashwin. "Next Word Prediction using Markov Model."](https://medium.com/ymedialabs-innovation/next-word-prediction-using-markov-model-570fc0475f96)
- [Veritasium. "The Strange Math that Predicts (Almost) Anything."](https://www.youtube.com/watch?v=KZeIEiBrT_w)

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

# How I Developed This Project

# Reflections

- I kind of didn't need to add orders when considering the list

- This is probably formatted wrong and doesn't consider the right audience

# notes

- To do:

    - Explain the code behind this markov chain

    - Explain the software engineering skills I learned/practiced

    - Explain how I developed the project (top-down, bottom-up, unit tests)

    - Create terminology to make code more coherent

    - Refactor and then reorganize code (?)

    - Write more tests

    - Reorganize README.md

    - List each file and explain how they work

    - Do I add `markov_data` to gitignore?

    - Add user manual

- How a probability list is stored
    
    - Stored as a list

    - Even-numbered indices `[0], [2], ...` have a token element `"k"`

    - The element following a token element is its weighted probability `0.02`

    - The sum of a probability list's weighted probabilities should be `1.0`

    - A token can be `"END"`, which causes the markov chain to terminate

- How a token map is stored

    - Stored as a list

    - Even-numbered indices `[0], [2], ...` have a token element `"s" or "sc"`

    - The element following a token element is a unique probability table

- How a markov chain is stored

    - Stored as a list

    - `markov[0]`: A probability list of starting tokens.

    - `markov[1]`: A probability list of first-order tokens (i.e. the second character of a word).

    - `markov[2]`: A probability list of second-order tokens.

- How a markov chain is written

    - `# TEXT` Serves as a flag to help adjust the code's behavior as it reads the text

    - Probability lists are stored on a linear line

    - Token maps are stored on different lines; each line is an element

    - For the following example, these will appear (but not in the actual .txt file):

        - `//` serves as an artificial comment line

        - `...` denotes redundant information

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