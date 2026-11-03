"""
Lets you create a second-order markov chain that can generate words.

@author Rookie
"""

import random
import json

# Markov chain custom global variables
ORDER = 2
IGNORE_CASE = False
COUNT_DUPES = False

CHAR_START = "__START__"
CHAR_END = "__END__"
CHAR_ORDER = "__ORDER__"
KEY_COUNT = "pathmap_count"
KEY_PATHMAP = "pathmap"

PATH_EXT_INPUT = ".txt"
PATH_EXT_CACHE = ".kov"

DIA_CHOOSE_FILE = "Choose a file to analyze: "
DIA_CHOOSE_FILE_AGAIN = "Invalid path. Try again: "
DIA_LOAD_MARKOV = "Markov chain loaded!\n"
DIA_INSTRUCTIONS = "Use these options to generate words:\n" + \
	" - Type in a number to use a seed, generating the same word.\n" + \
	" - Hit ENTER (or type in anything else) to generate a new word.\n" + \
	" - Type 'exit' or 'end' to stop this program.\n"

QUITTER_KEYS = {"exit", "exit()", "end"}

# General helper functions
def _file_exists(path):
	"""
	Returns whether or not the file exists.
	"""
	try:
		with open(path) as _:
			return True
	except FileNotFoundError:
		return False

def _float_safe(str):
	"""
	Like `float()`, but returns `None` instead of throwing a
	`ValueError` if the function fails.
	"""
	try:
		return float(str)
	except ValueError:
		return None

def _choose_from_prob(prob_dict):
	"""
	Chooses a key from a dictionary representing a probability distribution.

	Each key has a float value. The sum of all float values in this dictionary
	should be 1.0. A key will be returned more frequently if its paired value
	is higher.

	`{"a": 0.2, "b": 0.8}` => "b" 80% of the time, and "a" 20% of the time.
	"""

	x_r = random.random()	# For selecting weighted probabilities.
	x = 0.0					# Will increase until `x_r` is strictly less than this.

	for k, v in prob_dict.items():
		x += v
		if (x > x_r):		# Return first key that exceeds `x_r`
			return k

# Primary helper functions
def _translate_word(word, order=ORDER):
	"""
	Analyzes the character sequence of a single word.

	Returns a path-map, represented as a dictionary. Each key 
	is each current state in the word, and each value is the next
	state in the word. The current state's next state(s) are what
	the next letter is in the word.

	`"cat"` => `{<CHAR_START>: ["c"],  "c": ["a"],  "ca": ["t"],  "at": [<CHAR_END>]}`
	"""
	# Initialize
	pathmap = dict()
	for i in range(len(word) + 1):
		# Read the current character or <CHAR_END>
		next_state = CHAR_END if (i >= len(word)) else word[i]
		# Get the `order` previous characters or <CHAR_START>
		cur_state = word[max(i - order, 0):i] if ((i - max(i - order, 0) > 0)) else CHAR_START
		# Add to the dictionary
		if not (cur_state in pathmap):
			pathmap[cur_state] = list()
		pathmap[cur_state].append(next_state)
	# Return
	return pathmap

def _translate_text(text, order=ORDER, eliminate_case=IGNORE_CASE, count_dupes=COUNT_DUPES):
	"""
	Analyzes a string of multiple words `text` and assigns a
	pathmap to each one of them.

	Returns a dictionary:
	- The keys are the words that it encounters.
	- The values are a sub-dictionary:
		- Has the number of times the corresponding key was counted
		- Has the pathmap of the corresponding key
	"""
	# Initialize list of words
	pathmap_dict = dict()
	words = text.split()
	# Iterate over words
	for word in words:
		# Get the word, then filter it
		used_word = word if not eliminate_case else word.lower()
		# Translate word and add to entry
		pathmap = _translate_word(used_word, order)
		if not (used_word in pathmap_dict):
			new_word_entry = dict()
			new_word_entry[KEY_COUNT] = 1
			new_word_entry[KEY_PATHMAP] = pathmap
			pathmap_dict[used_word] = new_word_entry
		else:
			if (count_dupes):
				word_entry = pathmap_dict[used_word]
				word_entry[KEY_COUNT] = word_entry[KEY_COUNT] + 1
			
	return pathmap_dict

def _analyze_text(text, order=ORDER, eliminate_case=IGNORE_CASE, count_dupes=COUNT_DUPES):
	"""
	Analyzes a String of words `text`, and creates a probabilistic model for
	all of the current states and their next states.

	Returns a dictionary:
	- The keys represent all of the current states found in the
	`translate_text()` analysis. 
	- The values contain a sub-dictionary representing how frequently
	a certain next state will occur (a probability distribution).
		- Each key in the sub-dictionary is a next state.
		- A value in the sub-dictionary is a float. The sum of the values in the
	sub-dictionary is 1.0.
	"""
	# Initialize
	markov_dict = dict()
	pathmap_dict = _translate_text(text, order, eliminate_case, count_dupes)

	# Create `cur_state`-`next_state` pairs
	# Extract pathmaps from `pathmap_dict`
	pathmap_list = [
		pathmap_raw[KEY_PATHMAP]
		for pathmap_raw in pathmap_dict.values()
		for _ in range(pathmap_raw[KEY_COUNT])
	]
	# Create pairs
	cur_next_pairs = [
		(cur_state, next_state)
		for pathmap in pathmap_list
		for cur_state, next_state_list in pathmap.items()
		for next_state in next_state_list
	]
	
	# Iterate over each recorded `cur_state`-`next_state` pair
	for cur_next_pair in cur_next_pairs:
		cur_state = cur_next_pair[0]
		next_state = cur_next_pair[1]
		# Add/get a probability list
		if not (cur_state in markov_dict):
			markov_dict[cur_state] = dict()
		probability_list = markov_dict[cur_state]
		# Add the value
		if not (next_state in probability_list):
			probability_list[next_state] = 0
		probability_list[next_state] = probability_list[next_state] + 1

	# Normalize
	for probability_list_key in markov_dict:
		probability_list = markov_dict[probability_list_key]
		sum = 0
		for val in probability_list:
			sum += probability_list[val]
		for val in probability_list:
			probability_list[val] = probability_list[val] / sum

	markov_dict[CHAR_ORDER] = order

	return markov_dict

# If you are importing, please use these functions
def generate(markov, seed=None):
	"""
	Generates a word using a `markov` chain.
	"""
	output = ""

	order = markov[CHAR_ORDER]

	if (not seed):
		random.seed(seed)

	sentinel = True
	while (sentinel):
		# Get cur_state
		len_output = len(output)
		cur_state = output[len_output - order:len_output] if (len_output >= order) else (output if (len_output > 0) else CHAR_START)

		# Get probability list
		probability_list = markov[cur_state]

		# Pick a letter
		token = _choose_from_prob(probability_list)

		# Attach the letter to the output (or terminate if false)
		if (token == CHAR_END):
			sentinel = False
		else:
			output += token

	return output

def load(path):
	"""
	Returns a markov chain after running analysis on text from a file.

	Also stores a cache file in case the same file is loaded in the future.
	"""
	path_file = path + PATH_EXT_INPUT
	path_json = path + PATH_EXT_CACHE
	# Check the existence of a cache
	json_exists = _file_exists(path_json)
	# Return the cache if it exists
	if (json_exists):
		cache_contents = ""
		with open(path_json) as file:
			cache_contents = file.read()
		return json.loads(cache_contents)
	# Analyze the text
	txt = ""
	with open(path_file) as file:
		txt = file.read()
	output = _analyze_text(txt)
	# Create cache
	cache_contents = json.dumps(output)
	with open(path_json, "w") as file:
		file.write(cache_contents)

	return output

def main():
	"""
	Demonstrates the capabilities of this module.
	"""
	# Intro (and load chain)
	path = input(DIA_CHOOSE_FILE)
	print()
	sentinel_file = not _file_exists(path + PATH_EXT_INPUT)
	while sentinel_file:
		path = input(DIA_CHOOSE_FILE_AGAIN)
		print()
		sentinel_file = not _file_exists(path + PATH_EXT_INPUT)
	markov = load(path) # markov.load_markov
	print(DIA_LOAD_MARKOV)
	print(DIA_INSTRUCTIONS)

	# Loop
	sentinel_generation = True
	while (sentinel_generation):
		# Ask for input
		entry = input("Input: ")
		# Interpret input
		float_entry = _float_safe(entry)
		if (entry.lower() in QUITTER_KEYS):
			sentinel_generation = False
		elif not (float_entry):
			print("Output: " + generate(markov, seed=float_entry))
		else:
			print("Output: " + generate(markov))
		print()
	print("Program complete!")

if (__name__ == "__main__"):
    main()