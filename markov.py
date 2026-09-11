"""
Create a second-order markov chain that can generate words.
@author Rookie
"""

"""
Things to do:

    - How is a markov list generated?

    - Outline functions, top-down

    - Assertions for debugging

    - Verify that there are no missing invokes

    - Create tests + Program functions, down-top

    - Polish README.md, the bullet points for notes look weird

    - Add explanations and methodology to README.md

        - How does the markov chain work? (use terminology to update code)
"""

def analyze_word_to_tokens(word):
    """
    Takes a string `word` and does a second order markov analysis on it.

    "Table" --> ["START", "t", "t", "a", "ta", "b", "ab", "l", "bl", "e", "le", "END"]
    """

    # Initialize the list.

    # for loop: 0 to length - 1
        # is index 0?
            # Add "START" and word[i].
        # is index 1?
            # Add word[i - 1] and word[i].
        # is index >= 2?
            # Add word[i - 2] + word[i - 1] and word[i].
    # Add word[len - 2] + word[len - 1] and "END".

    # Return the list.
    ...

def get_markov_chain_item(markov_list, order, key, token):
    """
    Returns a numerical element from `markov_list`, specifically from the
    `order`th order, accessing with a context key `key`, for the probability of
    `token`.
    """
    # Access the ordered token map of the markov list.
    # Run a for loop on the token map.
        # Did you find the corresponding key in the token map?
            # Run a for loop on the corresponding probability list.
                # Did you find the corresponding token?
                    # Return the numerical element.
    # Return nothing.
    ...

def set_markov_chain_item(markov_list, order, key, token, value):
    """
    Sets an element's value of a `markov_list` given an `order`, context `key`,
    and the `token` which needs its numerical element set to `value`.
    """
    # Access the ordered token map of the markov list.
    # Run a for loop on the token map.
        # Did you find the corresponding key in the token map?
            # Run a for loop on the corresponding probability list.
                # Did you find the corresponding token?
                    # Set the numerical element.
                    # Return True.
    # Return False.
    ...

def increment_markov_chain_item(markov_list, order, key, token):
    """
    Uses `set_markov_chain_item` to increase a numerical element by 1.
    """
    # Store a variable through invoking `get_markov_chain_item`.
    # Increment the variable by 1.
    # Invoke `set_markov_chain_item` with the new variable.
    ...

def assimilate_into_markov_chain(markov_list, token_analysis):
    """
    Uses the list `token_analysis`, then adds its frequency (int) to `markov_list`.
    """
    # Is the analysis at least two elements long?
        # Invoke `increment_markov_chain_item` for order 0, key START, token (analysis[1]).
    # Is the analysis at least four elements long?
        # Invoke `increment_markov_chain_item` for order 1, key a[2], token a[3].
    # Is the analysis at least six elements long?
        # Run a modified for loop
            # For each second-ordered token, invoke increment, order 2, key a[n], token a[n + 1].
    ...

def sum_probability_list(probability_list):
    """
    Returns the sum of the numerical elements in a `probability_list`.
    """
    # Initialize a variable to get the sum.
    # Run a modified for loop on the probability list.
        # Add the value of each numerical element to the sum.
    # Return the sum variable's value.
    ...

def normalize_probability_list(probability_list):
    """
    Divides all numerical elements in `probability_list` such that the sum of
    all the numerical elements will equal 1.0.
    """
    # Initialize a variable to get the sum of the probability list.
    # Invoke `sum_probability_list`. 
    # Run a modified for loop on the probability list.
        # Divide each element by the sum, then set each element to the quotient.
    # Return the new probability list.
    ...

def normalize_markov_list(markov_list):
    """
    Normalizes a markov list's probability lists.
    """
    # Run a for loop on markov_list to get its token maps.
        # Run a modified for loop on each token map to get its probability lists.
            # Invoke `normalize_probability_list` to set each probability list.

    # Return the markov list.
    ...

def make_markov_network():
    """
    Returns a [markov chain] after reading a hardcoded text file.
    """

    # Create a markov chain: a list of three token maps.

    # Use `with as` to open the file.
        # Run a for loop on each line of the file.
            # Strips each line.
            # Get an analysis of a word's patterns through `analyze_word_to_tokens`.
            # Use the analysis by invoking `assimilate_into_markov_chain`.
    
    # Normalize the frequency of the markov chain.

    # Return the markov chain.
    ...

def write_probability_list(probability_list):
    """
    Takes a stored `probability_list` and returns a string representation of it.
    """
    # Initialize the representative string.

    while False: # For loop
        # Use str() to add a " " to the string.
        # If it's not the end of the list, add " ".
        ...
    
    # Return the string.

def write_network(markov_list):
    """
    Takes a stored `markov_list` and overwrites it to "markov_data.txt"
    """

    # initialize a string to be stored into a file.

    while False: # for each order in the markov chain:
        # Write the double hashtag header
        # Write each element of each token map on a separate line, partly through `write_probability_list`
        ...
    ...

def read_network_file_each_line(markov_list, line):
    # CODE
    # If there's a #
        # Append a new token map to the markov chain
    # Otherwise
        # If the len(split) == 1
            # Add the line to the most recent token map
        # Else
            # Split the line into a probability list and add it to the most recent token map
    # Return the markov_list, just in case
    # A refactoring may need to remove the above line
    ...

def read_network_file():
    """
    Reads "markov_data.txt" and returns a stored markov chain.
    """

    # SETUP
    # The markov chain to return
    # The current token map to store into a markov[#]

    # DODE
    # Open the file through a `with as`
        # Run a for loop on the file
            # Strip the line for cleanliness
            # Invoke `markov_chain = read_network_file_each_line` to prevent overnesting
    # Return markov list
    ...

def find_probability_list(markov_list, order, token):
    """
    Chooses a token map from `markov_list` based on the `order`th order of tokens.

    Uses `token` as the key.
    """

    # Start analyzing markov_list[order]

    while False: # for loop with index and skip 2
        # Does `index` have the `token`?
        # If so, return the probability list at `index + 1`
        ...
    # Throw up

def choose_random_token(probability_list):
    """
    Chooses a random token from `probability_list`.
    """

    # Generate a random number of set [0.0, 1.0)
    # Generate a "right boundary" count
        # It will be 1.0 at the end of the loop

    while False: # should instead be a for loop with an index, as well as skip 2
        # Add the element of `index + 1` (the probability) to the right boundary
        # If the earlier-set random number is NOW less than the right boundary, return element of `index`
        ...

def use_markov_network(markov_list):
    """
    Returns a String generated by a [markov chain] `markov_list`.
    """

    # SETUP
    # Var: The string to return
    # Var: Context variable to select tokens

    # CODE
    # Choose a probability list from markov_list[0] using `find_probability_list`
    # Invoke `choose_random_token` for the probability list, then get the token
    # If "END" has been pulled, return ""
    # Set the context to the first character
    # Choose a probability list from markov_list[1]
    # Invoke `choose_random_token` for the probability list, then get the token
    # If "END", return "#"
    # Set the context to the first and second character
    
    while False: # Loop for the second order Markov Chain
        # Choose a probability list from markov_list[2]
        # Invoke `choose_random_token` for the probability list, then get the token
        # If "END", return string
        # Set the context to the second character of the old one, and the new character combined
        ...

def main():
    """
    Prompts the user to type "make" to make the markov chain or "use" to run the markov chain.
    """
    # Set a blank string variable for the input
    # Get a loop that is broken once the string variable is empty
    while False:
        # Prompt the user to type "make" or "use"
        # If neither is used, repeat
        ...
    # If make, invoke `write_network` and `make_markov_network`
    # If use, invoke `read_network_file`, `use_markov_network`, and `print`
    ...

if (__name__ == "__main__"):
    main()