import markov.py

# Auxillary
def search_list_for_element(a_list, an_element):
    """
    Returns `True` if `an_element` (preferably not a list) can be found in `a_list`.
    """
    # Run a for loop.
        # Is each element equal to an_element?
            # Return true.
    # Return false.

def compare_matching_lists(list_a, list_b):
    """
    Determines if all elements of `list_a` can be found in `list_b` and vice versa.
    """

    # Run a for loop on list A.
        # Can each element be found in list_b through invoking `search_list_for_element`?
    ...

# Metatests

# Tests
"""def test_analyze_word_to_tokens():
    # setup
    word = "table"
    expected = ["START", "t", "t", "a", "ta", "b", "ab", "l", "bl", "e", "le", "END"]

    # invoke
    actual = markov.analyze_word_to_tokens(word)

    # analyze
    # assert expected == actual"""