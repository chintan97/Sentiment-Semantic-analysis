from os import listdir
from os.path import isfile, join
import os
import json
import re

# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
# It will fetch all files available in the input folder. It contains all .sgm files
files = [file for file in listdir("./input/") if isfile(join("./input/", file))]

data_to_write = {}   # This will contains json structure as document number: article data

document_count = 1   # Just to assign document number to each documents

for file in files:
    open_file = open("./input/" + file, "r")
    file_data = open_file.read()
    # Each document has actual article data in <BODY> tag. So fetch data and store in list
    # https://docs.python.org/2/library/re.html
    body_tag_data = re.compile('<BODY>(.*?)</BODY>', re.DOTALL).findall(file_data)  # Fetch content of body tag as it contains actual article contents and store in list
    for document_data in body_tag_data:
        data_to_write["document " + str(document_count)] = document_data   # json format will be like document 1: <article data>
        document_count += 1

print("Total documents generated: " + str(document_count-1))
# Create document folder if it is not available, else it will be overwritten
if not os.path.exists('./document'):
    os.makedirs('./document')

with open("./document/documents.json", "w") as document_file:
    json.dump(data_to_write, document_file)   # Write whole json into file. This file will used in semantic_analysis.py