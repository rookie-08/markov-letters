# markov-letters

Using Python to create a second-order markov chain that can generate words.

# notes

- To do:

    - Provide background information as to how Markov Chains work

    - Identify inspiration of second order markov chains

    - Explain how Markov chains work in this specific case

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