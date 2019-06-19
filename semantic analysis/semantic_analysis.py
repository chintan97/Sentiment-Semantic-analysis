import re
import math
import json
import os

file = open("./document/documents.json", "r")   # Open file which was generated from generate_documents.py

data = json.load(file)   # It contains content of file in json format

total_documents = len(data)   # Total number of documents which will be used in calculation of IDF
TF_matrix = {}  # To store TF values
count_occurence_matrix = {}  # To store: in how many documents, a word is occuring.
                             # It will be used in calculation of IDF

log_values_IDF = {}  # To store IDF values
TF_IDF = {}  # To store TF*IDF
cosine_similarity_dict = {}  # To store cosine similarity between document and query

for key, document in data.items():
    document_key_list = {}   # It will store all keys appeared in a particular document
    # Below code will process document data to remove special characters and emoticons if available
    document = document.strip()
    document = document.replace("\\u", '')
    document = document.replace("\n", ' ')
    document = re.sub(r'[^A-Za-z0-9 ]+', '', document)
    document = document.lower()   # Convert all words to lower so that parsing can be easy
    words = document.split()  # Split whole document after transforming it to lower and stripped
    for word in words:
        if word not in document_key_list:   # It is a new key. So store with key: 1
            document_key_list[word] = 1
        else:    # The key is already available in document. Thus just increment count
            document_key_list[word] += 1

    # Here for TF_matrix, instead of considering all keywords of all documents,
    # I am just considering words which are available in
    # particular document. So, instead of taking all columns and increasing matrix dimensions,
    # I am considering those columns which have values other than 0.
    # Because if a keyword is not present in document, it will store 0. 0 can be ignored as they
    # will not affect further calculation because they will be multiplied and give 0.
    TF_matrix[key] = document_key_list
    for keyword, value in document_key_list.items():
        if keyword not in count_occurence_matrix:   # The word is new, so assign 1
            count_occurence_matrix[keyword] = 1
        else:   # The word is already present, so just increment count value
            count_occurence_matrix[keyword] += 1

# Now, calculate log values for IDF matrix. As count_occurence_matrix has all unique words, we will directly
# apply IDF formula on it.
for key, value in count_occurence_matrix.items():
    log_values_IDF[key] = math.log(float(total_documents / value), 2)   # total documents divide by in how many documents a word occured with log base 2

for key, value in TF_matrix.items():
    temp_dictionary = {}
    for word, occurence in value.items():
        temp_dictionary[word] = occurence * log_values_IDF[word]
    TF_IDF[key] = temp_dictionary   # TF_IDF has same dimensions as TF_matrix. But it stores TF * IDF values

query = "canada"
# In TF * IDF matrix of query, just one columns 'canada' will have value other than 0.
# So, instead of making matrix with no meaning (values will be multiplied with 0 and give 0) for further calculation,
# I am just using variable.
TF_IDF_query = float(1 / count_occurence_matrix.get("canada")) * log_values_IDF.get("canada")

# Now, for cosine similarity, first we will calculate distance of documents and use it in cosine similarity.
# Here, it is not needed to calculate distance for query as it has only one word.
for key, value in TF_IDF.items():
    square_sum = 0   # to store sum of square of TF_IDF
    for word, TF_IDF_value in value.items():
        square_sum += TF_IDF_value ** 2

    if "canada" in value.keys():   # If 'canada' is in document, then only cosine will have value other than 0
        multiply_query_document_TF_IDF = TF_IDF_query * value.get("canada")
    else:   # If 'canada' is not in document, we will get 0 as cosine
        multiply_query_document_TF_IDF = 0
    cosine_similarity_dict[key] = multiply_query_document_TF_IDF / (math.sqrt(square_sum) * TF_IDF_query)

cosine_list_with_more_than_zero = []   # It will store only documents with cosine values more than 0.
for key, value in cosine_similarity_dict.items():
    if value > 0:
        cosine_list_with_more_than_zero.append([key, value])   # store with document number and cosine value

# https://stackoverflow.com/questions/18563680/sorting-2d-list-python
# Sort list according to cosine value. First in list will have highest rank
rank_list = sorted(cosine_list_with_more_than_zero, key=lambda l:l[1], reverse=True)

# Create output folder if it is not available, else it will be overwritten
if not os.path.exists('./output'):
    os.makedirs('./output')

# Now, I am making txt files which contain article texts and storing in output folder.
# Filename as 1.txt is having first rank and so on.
rank_count = 1
for list in rank_list:
    document_number = list[0]
    with open("./output/" + str(rank_count) + ".txt", "w") as file:
        file.write(data.get(document_number))
        file.close()
    rank_count += 1