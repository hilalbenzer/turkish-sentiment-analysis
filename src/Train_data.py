import re, os
import numpy as np
from TurkishStemmer import TurkishStemmer
import time
import pickle
import Util
from spell_correction import correction
from pathlib import Path

stemmer = TurkishStemmer()
src_folder = Path("./")
stopwords = Util.read_file(Path(src_folder / "stopwords.txt")).split("\n")
#exclude = [".", ",", ":", ";", "?", "!", "\"", "#", "$", "%", "&", "\'", "\(", "\)", "\*", "+", "-", "\\", "/", "<", ">", "=", "@", "[", "]", "\^", "_", "`", "{", "}", "|", "~"]

def preprocess(text):
	delete_list = [",", "’"]
	tweet = Util.delete_characters_space(text, delete_list)
	word_list = tweet.split()
	word_list = [ Util.stem_word(correction.correction(Util.remove_punct(Util.remove_repeating_char(Util.remove_with_regex(word))))) for word in word_list ]
	word_list = [word for word in word_list if len(word) > 1]
	word_list = Util.remove_words(word_list, stopwords)

	sentence = ""
	for word in word_list:
		sentence = sentence + " " + word
		Util.add_to_freq_dict(dictionary, word)

	return(sentence)

def create_train(text_raw, tag):
	text_lines = text_raw.split("\n")

	for line in text_lines:
		line = line.lower()
		tweet = line.split("\t")[3]

		sentence = preprocess(tweet)
		tup = (sentence, tag)
		train.append(tup)

start = time.time()

direct = src_folder / "TrainFirstHalf"
print("TRAIN")
print("Reading files...")
positive_raw = Util.read_file(os.path.join(direct, "positive-train"))
negative_raw = Util.read_file(os.path.join(direct, "negative-train"))
notr_raw = Util.read_file(os.path.join(direct, "notr-train"))

print("Preprocessing...")
train = []
data = []
labels = []

dictionary = {}
create_train(negative_raw, 0)
create_train(notr_raw, 1)
create_train(positive_raw, 2)

#Util.write_file("dictionary", dictionary)

for x, y in train:
    data.append(x)
    labels.append(y)

print("Creating pickle files...")
def create_pickle(filename, output):
    outfile = open(filename, 'wb')
    pickle.dump(output, outfile)
    outfile.close()

create_pickle("dataTrain", data)
create_pickle("labelsTrain", labels)

direct = src_folder / "TrainSecondHalf"
print("\nTEST")
print("Reading files...")
positive_raw = Util.read_file(os.path.join(direct, "positive-train"))
negative_raw = Util.read_file(os.path.join(direct, "negative-train"))
notr_raw = Util.read_file(os.path.join(direct, "notr-train"))

print("Preprocessing...")
train = []
data = []
labels = []

dictionary = {}
create_train(negative_raw, 0)
create_train(notr_raw, 1)
create_train(positive_raw, 2)

for x, y in train:
    data.append(x)
    labels.append(y)

print("Creating pickle files...")
def create_pickle(filename, output):
    outfile = open(filename, 'wb')
    pickle.dump(output, outfile)
    outfile.close()

create_pickle("dataTest", data)
create_pickle("labelsTest", labels)

end = time.time()
print("Elapsed time: " + str(end - start))
