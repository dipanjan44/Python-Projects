import os
import nltk
from nltk.util import ngrams

# Store the number of terms in each document in a separate data structure

corpus_location = "/Users/dipanjan/PycharmProjects/Python/IR3/TestFiles/"
Unigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Unigram"
Bigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Bigram"
Trigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Trigram"


# Write the contents of the Unigram to files
def write_uni_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_key=filename.split(".")[0]
    unigram_final_list_folder=os.path.join(file_location,"UnigramList.txt")
    unigram_final_list=open(unigram_final_list_folder,"a+")
    current_file = open(folder, "a+")
    current_file.write("Term" + " : " +"Term-Frequency" + "\n")
    unigram_counter=0
    for key, value in corpus_map.items():
        unigram = key[0] + " : "  + str(value)
        unigram_counter=unigram_counter+1
        current_file.write(str(unigram))
        current_file.write("\n")
    # Write the DocName and total number of unique unigrams in the doc to the outfile UnigramList.txt"
    unigram_final_list.write("{ " +str(file_key) +" : " +str(unigram_counter) + " }" +"\n")
    unigram_final_list.close()
    current_file.close()


# Write the contents of the Bigram to files
def write_bi_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, documentID, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_key = filename.split (".")[0]
    bigram_final_list_folder = os.path.join (file_location, "BigramList.txt")
    bigram_final_list = open (bigram_final_list_folder, "a+")
    current_file = open(folder, "a+")
    current_file.write ("Term" + " : " + "Term-Frequency" + "\n")
    bigram_counter = 0
    for key, value in corpus_map.items():
        bigram= ' '.join(str(k) for k in key)
        temp_string = "(" + bigram + ")" + ": " + str(value)
        bigram_counter = bigram_counter + 1
        current_file.write(str(temp_string))
        current_file.write("\n")
    # Write the DocName and total number of unique bigrams in the doc to the outfile BigramList.txt"
    bigram_final_list.write ("{ " + str (file_key) + " : " + str (bigram_counter) + " }" + "\n")
    bigram_final_list.close ()
    current_file.close()


# Write the contents of the Trigram to files
def write_tri_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, documentID, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_key = filename.split (".")[0]
    trigram_final_list_folder = os.path.join (file_location, "TrigramList.txt")
    trigram_final_list = open (trigram_final_list_folder, "a+")
    current_file = open (folder, "a+")
    current_file.write ("Term" + " : " + "Term-Frequency" + "\n")
    trigram_counter = 0
    for key, value in corpus_map.items():
        trigram = ' '.join(str(k) for k in key)
        temp_string = "(" + trigram + ")" + " : "  + str(value)
        trigram_counter=trigram_counter+1
        current_file.write(str(temp_string))
        current_file.write("\n")
    # Write the DocName and total number of unique trigrams in the doc to the outfile TrigramList.txt"
    trigram_final_list.write ("{ " + str (file_key) + " : " + str (trigram_counter) + " }" + "\n")
    trigram_final_list.close ()
    current_file.close()


# Read the contents of the corpus
def store_n_grams(corpus_location):
    for filename in os.listdir(corpus_location):
        current_file = open(corpus_location + filename,'r')
        tokens = get_all_tokens(current_file)
        current_file.close()
        build_n_grams(tokens, filename)

# Convert the contents of the file to tokens
def get_all_tokens(current_file):
    file_content = current_file.read()
    file_tokens = file_content.split(" ")
    return file_tokens

# To generate n-grams (where n = 1, 2, 3) from the corpus
def build_n_grams(tokens, filename):
    build_unigrams(tokens, filename)
    build_bigrams(tokens, filename)
    build_trigrams(tokens, filename)

# To generate unigrams from the corpus
def build_unigrams(tokens, filename):
    unigrams = ngrams(tokens, 1)
    corpus_map = nltk.FreqDist(unigrams)
    write_uni_gram_contents(corpus_map, Unigram_Location, filename)

# To generate bigrams from the corpus
def build_bigrams(tokens, filename):
    bigrams = ngrams(tokens, 2)
    corpus_map = nltk.FreqDist(bigrams)
    write_bi_gram_contents(corpus_map, Bigram_Location, filename)


# To generate trigrams from the corpus
def build_trigrams(tokens, filename):
    trigrams = ngrams(tokens, 3)
    corpus_map = nltk.FreqDist(trigrams)
    write_tri_gram_contents(corpus_map, Trigram_Location, filename)

# Main Function
def main():
    store_n_grams(corpus_location)

if __name__ == "__main__":
    main()