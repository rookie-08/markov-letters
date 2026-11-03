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
KEY_COUNT = "count"
KEY_TOKEN_MAP = "token_map"

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
	Analyzes the patterns of the character sequence in a single word.

	`"cat"` => `{<CHAR_START>: "c",  "c": "a",  "ca": "t",  "at": <CHAR_END>}`
	"""
    
	token_map = dict()

	for i in range(len(word) + 1):
		# The value is the current character or <CHAR_END>
		c = CHAR_END
		if (i < len(word)):
			c = word[i]
		# Get the trailing context characters (or <CHAR_START>)
		i_rear = i - order
		if (i_rear < 0):
			i_rear = 0
		lead = word[i_rear:i]
		if (len(lead) == 0):
			lead = CHAR_START
		# Add to the dictionary
		if not (lead in token_map):
			token_map[lead] = list()
		token_map[lead].append(c)
	
	return token_map

def translate_text(text, order=ORDER, eliminate_case=ELIMINATE_CASE, count_dupes=COUNT_DUPES):
	"""
	Takes a large string `text` and returns all of the translations.

	Does not count duplicate words.
	"""
	# Initialize list of words
	output = dict()
	words = text.split()
	# Iterate over words
	for word in words:
		# Get the word, then filter it
		used_word = word
		if (eliminate_case):
			used_word = word.lower()
		# Translate word and add to entry
		token_map = translate_word(used_word, order)
		if not (used_word in output):
			new_word_entry = dict()
			new_word_entry[KEY_COUNT] = 1
			new_word_entry[KEY_TOKEN_MAP] = token_map
			output[used_word] = new_word_entry
		else:
			if (count_dupes):
				word_entry = output[used_word]
				word_entry[KEY_COUNT] = word_entry[KEY_COUNT] + 1
			
	return output

def count_text_patterns(text, order=ORDER, eliminate_case=ELIMINATE_CASE, count_dupes=COUNT_DUPES):
	"""
	Reads the text and analyes the amount of context -> value maps that happen.

	Returns a dictionary of possible context keys; each key points to
	the probability distribution of what the next character could be.
	"""
	# Initialize
	output = dict()

	translations = translate_text(text, order, eliminate_case, count_dupes)

	# Iterate over each entry in a token map
	for word_key in translations:
		word_entry = translations[word_key]
		word_count = word_entry[KEY_COUNT]
		token_map = word_entry[KEY_TOKEN_MAP]
		for _ in range(word_count):
			for value_context in token_map:
				value = token_map[value_context]
				for value2 in value:
					# For each entry in a token map...
					# Add/get a probability list
					if not (value_context in output):
						output[value_context] = dict()
					probability_list = output[value_context]
					# Add the value
					if not (value2 in probability_list):
						probability_list[value2] = 0
					probability_list[value2] = probability_list[value2] + 1

	# Normalize
	for probability_list_key in output:
		probability_list = output[probability_list_key]
		sum = 0
		for val in probability_list:
			sum += probability_list[val]
		for val in probability_list:
			probability_list[val] = probability_list[val] / sum

	return output

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
		# Get context
		context_value = CHAR_START
		len_output = len(output)
		if (len_output > 0 and len_output < order):
			context_value = "" + output
		if (len_output >= order):
			ind_1 = len_output
			ind_0 = ind_1 - order
			context_value = output[ind_0:ind_1]

		# Get probability list
		probability_list = markov[context_value]

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