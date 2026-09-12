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

import random

MARKOV_CHAIN_PATH = "markov_data.txt"
DATASET_PATH = "simple_words.txt"

MARKOV_CHAIN = []

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

    # Loop
    length_token_map = len(markov_chain[order])
    for even_index in range(0, length_token_map, 2):
        focused_key = markov_chain[order][even_index]
        # Conditional statement: Finding the key in the token map
        if (focused_key == key):
            # Return the probability list
            return markov_chain[order][even_index + 1]

    # Edge case: Found nothing
    empty_list = []
    markov_chain[order].append(key)
    markov_chain[order].append(empty_list)
    return empty_list

def get_property(markov_chain, order, key, token):
    """
    Returns a numerical element from `markov_chain`, specifically from the
    `order`th order, accessing with a context key `key`, for the probability of
    `token`.

    Returns `None` if a value cannot be found.
    """

    # Loop
    focused_probability_list = get_probability_list(markov_chain, order, key)
    length_probability_list = len(focused_probability_list)
    for even_index in range(0, length_probability_list, 2):
        focused_token = focused_probability_list[even_index]
        focused_value = focused_probability_list[even_index + 1]
        # Conditional statement: Found the token
        if (focused_token == token):
            return focused_value
    # There is no token
    focused_probability_list.append(token)
    focused_probability_list.append(0)
    return 0

def set_property(markov_chain, order, key, token, value):
    """
    Sets an element's value of a `markov_chain` given an `order`, context `key`,
    and the `token` which needs its numerical element set to `value`.

    Returns `True` if the operation was successful.
    """

    # Loop
    focused_probability_list = get_probability_list(markov_chain, order, key)
    length_probability_list = len(focused_probability_list)
    for even_index in range(0, length_probability_list, 2):
        focused_token = focused_probability_list[even_index]
        # Conditional statement: Found the token
        if (focused_token == token):
            focused_probability_list[even_index + 1] = value
            return True
    # There is no token
    focused_probability_list.append(token)
    focused_probability_list.append(value)
    return True

def add_property(markov_chain, order, key, token):
    """
    Uses `set_property` to increase a numerical element by 1.

    Returns `True` if the operation was successful.
    """

    # Loop
    focused_probability_list = get_probability_list(markov_chain, order, key)
    length_probability_list = len(focused_probability_list)
    for even_index in range(0, length_probability_list, 2):
        focused_token = focused_probability_list[even_index]
        # Conditional statement: Found the token
        if (focused_token == token):
            # Incremement the next element by one
            focused_probability_list[even_index + 1] = focused_probability_list[even_index + 1] + 1
            return True
    # There is no token
    focused_probability_list.append(token)
    focused_probability_list.append(1)
    return True

# Chain Manipulation
def add_tokens(markov_chain, token_list):
    """
    Uses the list `token_list`, then adds its frequency (int) to `markov_chain`.
    """
    length_token_list = len(token_list)
    for index in range(0, length_token_list, 2):
        # Code about setting the order of the token b/c of the first two letters
        order = int(index / 2)
        if (order > 2):
            order = 2
        # Increments
        add_property(markov_chain, order, token_list[index], token_list[index + 1])

def sum_probability_list(probability_list):
    """
    Returns the sum of the numerical elements in a `probability_list`.
    """

    sum = 0

    length_of_prob_list = len(probability_list)
    for odd_index in range(1, length_of_prob_list, 2):
        sum = sum + probability_list[odd_index]

    return sum

def normalize_probability_list(probability_list):
    """
    Divides all numerical elements in `probability_list` such that the sum of
    all the numerical elements will equal 1.0.
    """
    # Setup
    prev_sum_prob_list = sum_probability_list(probability_list)
    # Loop
    length_of_prob_list = len(probability_list)
    for odd_index in range(1, length_of_prob_list, 2):
        probability_list[odd_index] = probability_list[odd_index] / prev_sum_prob_list

def normalize_markov_chain(markov_chain):
    """
    Normalizes a markov chain's probability lists.
    """

    for token_map in markov_chain:
        length_token_map = len(token_map)
        for odd_index in range(1, length_token_map, 2):
            normalize_probability_list(token_map[odd_index])

# Application
def generate_token(probability_list):
    """
    Chooses a random token from `probability_list`.
    """
    a_float = random.random()   # For selecting weighted probabilities.
    right_boundary = 0.0        # Will increase until `a_float` is strictly less than this.

    for odd_index in range(1, len(probability_list), 2):
        right_boundary = right_boundary + probability_list[odd_index]
        if (a_float < right_boundary):
            return probability_list[odd_index - 1]
    # assert False, "Given float " + str(a_float) + " and boundary " + str(right_boundary) + ", something happened"

# Higher Order Actions
def from_file(): # UNSTABLE
    """
    Reads "markov_data.txt" and returns a stored markov chain.
    """

    # TODO: Write a function "is_markov_chain(markov_chain)"
    # TODO: Write tests

    markov_chain = []

    with open(MARKOV_CHAIN_PATH) as file:
        for raw_line in file:
            line = raw_line.strip()
            convert_fileline_to_chaindata(markov_chain, line)

    return markov_chain

def to_file(markov_chain): # UNSTABLE
    """
    Takes a stored `markov_chain` and overwrites it to "markov_data.txt"
    """

    # TODO: Write tests

    string_to_store = ""

    length_of_markov_chain = len(markov_chain)
    for order in range(length_of_markov_chain):
        # Append # ORDER N
        string_to_store = string_to_store + "# ORDER " + str(order) + "\n"
        token_map = markov_chain[token_map]
        for even_element in range(0, len(token_map), 2):
            prob_list = token_map[even_element + 1]
            # Append key
            string_to_store = string_to_store + token_map[even_element] + "\n"
            # Append probability list
            string_to_store = string_to_store + convert_probability_list_to_string(prob_list) + "\n"

def create_markov_chain(): # UNSTABLE
    """
    Returns a [markov chain] after reading a hardcoded text file.
    """

    markov_chain = [[], [], []]

    with open(DATASET_PATH) as file:
        for raw_line in file:
            line = raw_line.strip()
            token_list = convert_word_to_tokens(line)
            add_tokens(markov_chain, token_list)

    normalize_markov_chain(markov_chain)

    return markov_chain

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