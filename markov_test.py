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

    for element_a in list_a:
        included_element_a = search_list_for_element(list_b, element_a)
        if (not included_element_a):
            return False
    for element_b in list_b:
        included_element_b = search_list_for_element(list_a, element_b)
        if (not included_element_b):
            return False
    return True

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

def test_compare_matching_lists_1():
    # setup
    list_a = ["t", "t", "a", "a", "b", "b"]
    list_b = ["t", "t", "a", "a", "b", "b"]
    expected = True

    # invoke
    actual = compare_matching_lists(list_a, list_b)

    # analyze
    assert expected == actual

def test_compare_matching_lists_2():
    # setup
    list_a = []
    list_b = ["START", "c", "c", "a", "ca", "t", "at", "END"]
    expected = False

    # invoke
    actual = compare_matching_lists(list_a, list_b)

    # analyze
    assert expected == actual

def test_compare_matching_lists_3():
    # setup
    list_a = []
    list_b = []
    expected = True

    # invoke
    actual = compare_matching_lists(list_a, list_b)

    # analyze
    assert expected == actual

def test_compare_matching_lists_4():
    # setup
    list_a = ["happy", "sad"]
    list_b = ["medium", "happy"]
    expected = False

    # invoke
    actual = compare_matching_lists(list_a, list_b)

    # analyze
    assert expected == actual

# Tests
def test_convert_word_to_tokens_3():
    # setup
    word = "cat"
    expected = ["START", "c", "c", "a", "ca", "t", "at", "END"]

    # invoke
    actual = markov.convert_word_to_tokens(word)

    # analyze
    assert compare_matching_lists(expected, actual)

def test_convert_word_to_tokens_5():
    # setup
    word = "table"
    expected = ["START", "t", "t", "a", "ta", "b", "ab", "l", "bl", "e", "le", "END"]

    # invoke
    actual = markov.convert_word_to_tokens(word)

    # analyze
    assert compare_matching_lists(expected, actual)

def test_convert_word_to_tokens_2():
    # setup
    word = "at"
    expected = ["START", "a", "a", "t", "at", "END"]

    # invoke
    actual = markov.convert_word_to_tokens(word)

    # analyze
    assert compare_matching_lists(expected, actual)

def test_convert_word_to_tokens_1():
    # setup
    word = "i"
    expected = ["START", "i", "i", "END"]

    # invoke
    actual = markov.convert_word_to_tokens(word)

    # analyze
    assert compare_matching_lists(expected, actual)

def test_convert_word_to_tokens_0():
    # setup
    word = ""
    expected = ["START", "END"]

    # invoke
    actual = markov.convert_word_to_tokens(word)

    # analyze
    assert compare_matching_lists(expected, actual)

def test_convert_probability_list_to_string():
    # setup
    probability_list = ["a", 0.2, "b", 0.3, "c", 0.5]
    expected = "a 0.2 b 0.3 c 0.5"

    # invoke
    actual = markov.convert_probability_list_to_string(probability_list)

    # analyze
    assert expected == actual

def test_convert_probability_list_to_string_0():
    # setup
    probability_list = []
    expected = ""

    # invoke
    actual = markov.convert_probability_list_to_string(probability_list)

    # analyze
    assert expected == actual