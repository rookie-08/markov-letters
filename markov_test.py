import markov

# Auxillary
def search_list_for_element(a_list, an_element):
    """
    Returns `True` if `an_element` (preferably not a list) can be found in `a_list`.
    """
    for element_of_list in a_list:
        if (element_of_list == an_element):
            return True
    return False

def compare_matching_lists(list_a, list_b):
    """
    Determines if all elements of `list_a` can be found in `list_b` and vice versa.
    """

    # Run a for loop on list A.
        # Can each element be found in list_b through invoking `search_list_for_element`?
    ...

# Metatests
def test_search_list_for_element_abcde_d():
    # setup
    a_list = ["a", "b", "c", "d", "e"]
    an_element = "d"
    expected = True

    # invoke
    actual = search_list_for_element(a_list, an_element)

    # analyze
    assert expected == actual

def test_search_list_for_element_abcde_g():
    # setup
    a_list = ["a", "b", "c", "d", "e"]
    an_element = "g"
    expected = False

    # invoke
    actual = search_list_for_element(a_list, an_element)

    # analyze
    assert expected == actual

def test_search_list_for_element_words():
    # setup
    a_list = ["START", "ab", "END"]
    an_element = "END"
    expected = True

    # invoke
    actual = search_list_for_element(a_list, an_element)

    # analyze
    assert expected == actual

# Tests
"""def test_analyze_word_to_tokens():
    # setup
    word = "table"
    expected = ["START", "t", "t", "a", "ta", "b", "ab", "l", "bl", "e", "le", "END"]

    # invoke
    actual = markov.analyze_word_to_tokens(word)

    # analyze
    # assert expected == actual"""