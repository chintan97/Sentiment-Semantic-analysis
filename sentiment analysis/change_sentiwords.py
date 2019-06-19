# This file is to remove tags (a, n, r etc.) from sentiwords.txt
# The format of sentiwords.txt is word appened with grammar tag and its polarity in range of -1.0 to +1.0
# exa. amazing#a	0.71692
# The new format of this line will be:   amazing	0.71692
# After such formatting, they will be stored in sentiwords_new.json

import json

new_file = open("sentiwords_new.json", "w")

# to exclude repeatative words
word_dict = {}

with open("sentiwords.txt", "r") as file:
    content = file.readlines()

for line in content:
    if line[0] != "#":
        line = line.strip()
        strip_line = line.split("\t")  # split each line into two words, first as word and second as polarity of word
        first_word = strip_line[0][:-2]   # remove last 2 characters which contain tags
        first_word = first_word.replace("_", " ")   # The words with space were appened with _. Thus, I am replacing _ with space.
        first_word = first_word.lower()   # Convert word into lower case
        second_word = strip_line[1]   # Store polarity of word
        if hasattr(word_dict, first_word):
            pass
        else:
            word_dict[first_word] = second_word

# Store dictionary in sentiwords_new.json. The format will be {"word": "polarity of word"}
json.dump(word_dict, new_file)