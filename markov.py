"""
Create a second-order markov chain that can generate words.
@author Rookie
"""

"""
Things to do:

    - How is a markov chain generated?

    - Outline functions, top-down

    - Assertions for debugging

    - Verify that there are no missing invokes

    - Create tests + Program functions, down-top

    - Polish README.md, the bullet points for notes look weird

    - Add explanations and methodology to README.md

        - How does the markov chain work? (use terminology to update code)
"""

# Converting 
def convert_word_to_tokens(word):
    """
    Takes a string `word` and converts it to a specific list.

    The even-numbered elements of the list `[0], [2], ...` represent tokens
    in the hypothesis (in a markov chain, this is where you "start"). The
    odd-numbered elements of the list `[1], [3], ...` directly following the
    even-numbered elements represent tokens in the conclusion (in the markov
    chain, you would go from the "start" to the next step).

    Example output: `"cat" => ["START", "c", "c", "a", "ca", "t", "at", "END"]`

    If the length of `word` is `w`, the length of the table will be `2w + 2`.
    """

    # Setup
    token_list = []

    word_length = len(word)

    # Edge cases
    if (word_length == 0):
        return ["START", "END"]
    elif (word_length == 1):
        return ["START", word, word, "END"]

    # Main code
    for char_index in range(word_length):
        if (char_index == 0):   # "START", word[0]
            token_list.append("START")
            token_list.append(word[char_index])
        elif (char_index == 1): # word[1], word[0]
            token_list.append(word[char_index - 1])
            token_list.append(word[char_index])
        elif (char_index >= 2): # word[n - 2] + word[n - 1], word[n]
            token_list.append(word[char_index - 2] + word[char_index - 1])
            token_list.append(word[char_index])
                                # word[L - 2] + word[L - 1], "END"
    
    token_list.append(word[word_length - 2] + word[word_length - 1])
    token_list.append("END")

    return token_list

def convert_probability_list_to_string(probability_list):
    """
    Returns a string representation of `probability_list`, separating each element by spaces.
    """

    # Setup
    string_prob_list = ""

    # Loop
    probability_list_length = len(probability_list)
    for index in range(probability_list_length):
        # Acquisition
        element = probability_list[index]
        string_element = str(element)
        # Concatentation
        string_prob_list = string_prob_list + string_element
        if (index < probability_list_length - 1):
            string_prob_list = string_prob_list + " "

    # Return
    return string_prob_list

def filter_probability_list(probability_list):
    """
    Goes through a `probability_list`'s elements and runs `float()` on the
    odd-numbered elements.
    """

    length_of_prob_list = len(probability_list)

    for odd_index in range(1, length_of_prob_list, 2):
        element = probability_list[odd_index]
        num_element = float(element)
        probability_list[odd_index] = num_element

def convert_fileline_to_chaindata(markov_chain, line):
    """
    Adds data to `markov_chain` depending on the string `line` that it reads.

    - If `line` starts with #, a new list (token map) is appended to
    `markov_chain`.
    
    - If `line` consists of a one-word, non-#-starting String, it is added to
    the most recent token map.

    - If `line` doesn't start with # and is split into more than one word, it
    is converted to a list before being added to the most recent token map.
    """

    # Analysis
    length_markov_chain = len(markov_chain)
    starts_with_hash = (line[0] == "#")
    split_line = line.split(sep=" ")
    length_split_line = len(split_line)

    # Behavior
    if (starts_with_hash):
        new_token_map = []
        markov_chain.append(new_token_map)                              # Line starts with hashtag
    else:
        if (length_split_line == 1):
            markov_chain[length_markov_chain - 1].append(line)          # Line has only one word
        else:
            filter_probability_list(split_line)
            markov_chain[length_markov_chain - 1].append(split_line)    # Line has more than one word

# Manipulation
def get_probability_list(markov_chain, order, key):
    """
    Retrieves a probability list from the `order`th token map.

    Uses `token` as the key.

    Returns `[]` if a probability list cannot be found.
    """

    length_token_map = len(markov_chain[order])

    for even_index in range(0, length_token_map, 2):
        focused_key = markov_chain[order][even_index]
        if (focused_key == key):
            return markov_chain[order][even_index + 1]

    return []

def get_property(markov_chain, order, key, token):
    """
    Returns a numerical element from `markov_chain`, specifically from the
    `order`th order, accessing with a context key `key`, for the probability of
    `token`.

    Returns `None` if a value cannot be found.
    """

    focused_probability_list = get_probability_list(markov_chain, order, key)
    length_probability_list = len(focused_probability_list)

    for even_index in range(0, length_probability_list, 2):
        focused_token = focused_probability_list[even_index]
        focused_value = focused_probability_list[even_index + 1]
        if (focused_token == token):
            return focused_value

def set_property(markov_chain, order, key, token, value):
    """
    Sets an element's value of a `markov_chain` given an `order`, context `key`,
    and the `token` which needs its numerical element set to `value`.
    """
    # Access the ordered token map of the markov chain.
    # Run a for loop on the token map.
        # Did you find the corresponding key in the token map?
            # Run a for loop on the corresponding probability list.
                # Did you find the corresponding token?
                    # Set the numerical element.
                    # Return True.
    # Return False.

    focused_probability_list = get_probability_list(markov_chain, order, key)
    length_probability_list = len(focused_probability_list)

    for even_index in range(0, length_probability_list, 2):
        focused_token = focused_probability_list[even_index]
        if (focused_token == token):
            focused_probability_list[even_index + 1] = value
            return True
    return False

def add_property(markov_chain, order, key, token):
    """
    Uses `set_property` to increase a numerical element by 1.
    """
    # Store a variable through invoking `get_property`.
    # Increment the variable by 1.
    # Invoke `set_property` with the new variable.
    ...

# Chain Manipulation
def add_tokens(markov_chain, token_analysis):
    """
    Uses the list `token_analysis`, then adds its frequency (int) to `markov_chain`.
    """
    # Is the analysis at least two elements long?
        # Invoke `add_property` for order 0, key START, token (analysis[1]).
    # Is the analysis at least four elements long?
        # Invoke `add_property` for order 1, key a[2], token a[3].
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

def normalize_markov_chain(markov_chain):
    """
    Normalizes a markov chain's probability lists.
    """
    # Run a for loop on markov_chain to get its token maps.
        # Run a modified for loop on each token map to get its probability lists.
            # Invoke `normalize_probability_list` to set each probability list.

    # Return the markov chain.
    ...

# Application
def generate_token(probability_list):
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

# Higher Order Actions
def from_file():
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
            # Invoke `markov_chain = convert_fileline_to_chaindata` to prevent overnesting
    # Return markov chain
    ...

def to_file(markov_chain):
    """
    Takes a stored `markov_chain` and overwrites it to "markov_data.txt"
    """

    # initialize a string to be stored into a file.

    while False: # for each order in the markov chain:
        # Write the double hashtag header
        # Write each element of each token map on a separate line, partly through `covert_probability_list_to_string`
        ...
    ...

def create_markov_chain():
    """
    Returns a [markov chain] after reading a hardcoded text file.
    """

    # Create a markov chain: a list of three token maps.

    # Use `with as` to open the file.
        # Run a for loop on each line of the file.
            # Strips each line.
            # Get an analysis of a word's patterns through `convert_word_to_tokens`.
            # Use the analysis by invoking `add_tokens`.
    
    # Normalize the frequency of the markov chain.

    # Return the markov chain.
    ...

def generate_string(markov_chain):
    """
    Returns a String generated by a [markov chain] `markov_chain`.
    """

    # SETUP
    # Var: The string to return
    # Var: Context variable to select tokens

    # CODE
    # Choose a probability list from markov_chain[0] using `get_probability_list`
    # Invoke `generate_token` for the probability list, then get the token
    # If "END" has been pulled, return ""
    # Set the context to the first character
    # Choose a probability list from markov_chain[1]
    # Invoke `generate_token` for the probability list, then get the token
    # If "END", return "#"
    # Set the context to the first and second character
    
    while False: # Loop for the second order Markov Chain
        # Choose a probability list from markov_chain[2]
        # Invoke `generate_token` for the probability list, then get the token
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
    # If make, invoke `to_file` and `create_markov_chain`
    # If use, invoke `from_file`, `generate_string`, and `print`
    ...

if (__name__ == "__main__"):
    main()