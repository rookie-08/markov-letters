"""
Lets you create a second-order markov chain that can generate words.

@author Rookie
"""

import random
import json

# Markov chain custom global variables
ORDER = 2
ELIMINATE_CASE = False
COUNT_DUPES = False

CHAR_START = "START"
CHAR_END = "END"
KEY_COUNT = "pathmap_count"
KEY_PATHMAP = "pathmap"

PATH_EXT_INPUT = ".txt"
PATH_EXT_CACHE = ".kov"

DIA_CHOOSE_FILE = "Choose a file to analyze: "
DIA_LOAD_MARKOV = "Markov chain loaded!\n"
DIA_INSTRUCTIONS = "Use these options to generate words:\n" + \
	" - Type in a number to use a seed, generating the same word.\n" + \
	" - Hit ENTER (or type in anything else) to generate a new word.\n" + \
	" - Type 'exit' or 'end' to stop this program.\n"

QUITTER_KEYS = {"exit", "exit()", "end"}

# General helper functions
def file_exists(path):
	"""
	Returns whether or not the file exists.
	"""
	try:
		with open(path) as _:
			return True
	except FileNotFoundError:
		return False

def float_safe(str):
	"""
	Like `float()`, but returns `None` instead of throwing a
	`ValueError` if the function fails.
	"""
	try:
		return float(str)
	except ValueError:
		return None

# Primary helper functions
def translate_word(word, order=ORDER):
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

def translate_text(text, order=ORDER, eliminate_case=ELIMINATE_CASE, count_dupes=COUNT_DUPES):
	"""
	Analyzes a string of multiple words `text` and assigns a
	pathmap to each one of them.

	Returns a dictionary. Its keys are the words that it encounters.
	The values are a sub-dictionary that has both the number of words
	it came across and the pathmap of the word.
	"""
	# Initialize list of words
	pathmap_dict = dict()
	words = text.split()
	# Iterate over words
	for word in words:
		# Get the word, then filter it
		used_word = word if not eliminate_case else word.lower()
		# Translate word and add to entry
		pathmap = translate_word(used_word, order)
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

def count_text_patterns(text, order=ORDER, eliminate_case=ELIMINATE_CASE, count_dupes=COUNT_DUPES):
	"""
	Analyzes a String of words `text`, and creates a probabilistic model for
	all of the current states and their next states.

	Returns a dictionary. The keys represent all of the current states found
	in the `translate_text()` analysis. The values contain a dictionary
	representing how frequently a certain next state will occur given a
	current state. Each key in the sub-dictionary is a next state, while a
	value in the sub-dictionary is a float. The sum of the values in the
	sub-dictionary is 1.0.
	"""
	# Initialize
	markov_dict = dict()
	pathmap_dict = translate_text(text, order, eliminate_case, count_dupes)

	# Create `cur_state`-`next_state` pairs
	cur_next_pairs = list()
	for pathmap_raw in pathmap_dict.values():
		pathmap = pathmap_raw[KEY_PATHMAP]
		for _ in range(pathmap_raw[KEY_COUNT]):
			for cur_state in pathmap:
				for next_state in pathmap[cur_state]:
					cur_next_pair = (cur_state, next_state)
					cur_next_pairs.append(cur_next_pair)
	
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

	return markov_dict

def generate_token(probability_list):
	"""
	Chooses a random token from `probability_list`.
	"""
	a_float = random.random()   # For selecting weighted probabilities.
	right_boundary = 0.0        # Will increase until `a_float` is strictly less than this.

	for key in probability_list:
		right_boundary += probability_list[key]
		if (a_float < right_boundary):
			return key

    # assert False, "Given float " + str(a_float) + " and boundary " + str(right_boundary) + ", something happened"

def generate(markov, seed=None, order=ORDER):
	"""
	Generates a word using a markov chain.
	"""
	output = ""

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
		token = generate_token(probability_list)

		# Attach the letter to the output (or terminate if false)
		if (token == CHAR_END):
			sentinel = False
		else:
			output += token

	return output

def load_markov(path):
	"""
	Returns a markov chain after running analysis on text from a file.

	Also stores a cache file in case the same file is loaded in the future.
	"""
	path_file = path + PATH_EXT_INPUT
	path_json = path + PATH_EXT_CACHE
	# Check the existence of a cache
	json_exists = False
	try:
		with open(path_json) as file:
			json_exists = True
	except:
		json_exists = False
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
	output = count_text_patterns(txt)
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
	markov = load_markov(path) # markov.load_markov
	print(DIA_LOAD_MARKOV)
	print(DIA_INSTRUCTIONS)

	# Loop
	sentinel = True
	while (sentinel):
		# Ask for input
		entry = input("Input: ")
		# Interpret input
		float_entry = float_safe(entry)
		if (entry.lower() in QUITTER_KEYS):
			sentinel = False
		elif not (float_entry):
			print("Output: " + generate(markov, seed=float_entry))
		else:
			print("Output: " + generate(markov))
		print()
	print("Program complete!")

if (__name__ == "__main__"):
    main()