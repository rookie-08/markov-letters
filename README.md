# markov-letters

Using Python to create a second-order markov chain that can generate words.

# notes

- How a probability list is stored
    
    - Stored as a list

    - Even-numbered indices `[0], [2], ...` have a token element `"k"`

    - The element following a token element is its weighted probability `0.02`

    - The sum of a probability list's weighted probabilities should be `1.0`

    - A token can be `"END"`, which causes the markov chain to terminate

- How a markov chain is stored

    - Stored as a list

    - `markov[0]`: A probability list of starting tokens.

    - `markov[1]`: A probability list of first-order tokens (i.e. the second character of a word).

    - `markov[2]`: A probability list of second-order tokens.