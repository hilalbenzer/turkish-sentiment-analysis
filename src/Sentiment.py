#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os
import nltk
from nltk.tokenize import word_tokenize
import string #punctuation
from TurkishStemmer import TurkishStemmer
import time
import operator #for sorting dict
import pickle

def read_file(filename):
	f = open(filename, "r") 
	file_text = f.read()
	f.close()
	return file_text

def write_file(filename, output):
	full_filename = './' + filename + '.txt'
	file = open(full_filename, 'a')
	file.write(str(output))
	file.close()

def add_to_freq_dict(dictionary, word):
	if word not in dictionary:
		freq = 1
		dictionary[word] = freq
	else:
		dictionary[word] += 1

stemmer = TurkishStemmer()
stopwords = read_file("stopwords_new.txt").split("\n")
#exclude = [".", ",", ":", ";", "?", "!", "\"", "#", "$", "%", "&", "\'", "\(", "\)", "\*", "+", "-", "\\", "/", "<", ">", "=", "@", "[", "]", "\^", "_", "`", "{", "}", "|", "~"]

def delete_characters(text, char_list):
	for char in char_list:
		text = re.sub(char, '', text)
	return text

def delete_characters_space(text, char_list):
	for char in char_list:
		text = re.sub(char, ' ', text)
	return text

def remove_words(word_list, delete_list):
	return [word for word in word_list if word not in delete_list]

"""def remove_with_regex(word_list):
	new_word_list = []
	for word in word_list:
		#check = re.findall(r'(?:pic.twitter|^@|\d+|^rt$)', word)
		check = re.findall(r'(?:pic.twitter|^@|^rt$)', word)
		if not check:
			new_word_list.append(word)
	return new_word_list"""

def remove_with_regex(word):
	check = re.findall(r'(?:pic.twitter|^@|^rt$)', word)
	if check:
		word = ""
	return(word)

def remove_decimal(word):
	new_word_list = []
	for word in word_list:
		check = re.findall(r'(?:\d+)', word)
		if not check:
			new_word_list.append(word)
	return new_word_list

def replace_emoticon(word):
	check_pos = re.findall(r'(?::\)|:-\)|=\)|:D|:d|<3|\(:|:\'\)|\^\^|;\))', word)
	check_neg = re.findall(r'(:-\(|:\(|;\(|;-\(|=\(|:/|:\\|-_-)', word)
	if check_pos:
		#word = ":)"
		word = "SMILEYPOSITIVE"
	elif check_neg:
		#word = ":("
		word = "SMILEYNEGATIVE"
	return word

def remove_punct(word):
    exclude = set(string.punctuation)
    word = replace_emoticon(word)
    word = ''.join(ch for ch in word if ch not in exclude)
    return word

def replace_turkish_char(word):
	#corr = {'ş':'s', 'ç':'c', 'ğ':'g', 'ü':'u', 'ö':'o', 'ı':'i'}
	word = word.replace('ş','s')
	word = word.replace('ç','c')
	word = word.replace('ğ','g')
	word = word.replace('ü','u')
	word = word.replace('ö','o')
	word = word.replace('ı','i')
	return word

def remove_repeating_char(word):
    new_word = ""
    prev_char = ''
    for char in word:
    	if prev_char == char:
    		continue
    	new_word = new_word + char
    	prev_char = char
    return new_word

def preprocess(text):
	delete_list = [",", "’"]
	tweet = delete_characters_space(text, delete_list)
	word_list = tweet.split()
	word_list = [ replace_turkish_char(stemmer.stem(remove_punct(remove_with_regex(word)))) for word in word_list ]
	word_list = [word for word in word_list if len(word) > 1]
	word_list = remove_words(word_list, stopwords)

	sentence = ""
	for word in word_list:
		sentence = sentence + " " + word
		add_to_freq_dict(dictionary, word)

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

direct = "./Train/"

print("Reading files...")
positive_raw = read_file(os.path.join(direct, "positive-train"))
negative_raw = read_file(os.path.join(direct, "negative-train"))
notr_raw = read_file(os.path.join(direct, "notr-train"))

print("Preprocessing...")
train = []
dictionary = {}
create_train(positive_raw, "1")
create_train(negative_raw, "-1")
create_train(notr_raw, "0")


#sorted_d = sorted(dictionary.items(), key=operator.itemgetter(1),reverse=True)
#write_file("dictionary", sorted_d)

print("This thing...")

all_words = set(word for passage in train for word in word_tokenize(passage[0]))
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]
classifier = nltk.NaiveBayesClassifier.train(t)

#training_set = nltk.classify.apply_features(extract_features, train)
#classifier = nltk.NaiveBayesClassifier.train(training_set)



test_sentence = ["SKANDAL !! Boğaziçi ?nde PKK sloganları ve PKK'nın ne işi var? pic.twitter.com/aNE1FKR5BB", "Boğaziçi üni kapatılsın. Bence gereksiz Pkk yuvası", "Hayaller tamda istanbul bogaziçi universitesi", "Boğaziçi Üniversitesi - Tarih Bölümü kalpben <3", "Bugün Bogaziçi Üniversitesi Mithat Alam Film Merkezi'nde Hayko Cepkin'le söylesecegiz: pic.twitter.com/emNtHqGMQD 18.00 itibariyle baslariz.", "Boğaziçi Üniversitesi yds 2014 - Bildirimiz sunuluyor pic.twitter.com/W1i4wQrW3K"]

counter_nt = 0
counter_neg = 0
counter_pos = 0
for test, tag in train:
	#print(test)
	test = test.lower()

	sentence = preprocess(test)

	#print(sentence)

	test_sent_features = {word.lower(): (word in word_tokenize(sentence)) for word in all_words}
	#print(classifier.classify(test_sent_features))
	#print("\n")

	check_tag = classifier.classify(test_sent_features)
	if tag == check_tag:
		if tag == "1":
			counter_pos +=1
		elif tag == "0":
			counter_nt += 1
		elif tag == "-1":
			counter_neg += 1
	else:
		write_file("results", test)
		write_file("results", "olan " + tag)
		write_file("results", "bulunan " + check_tag)
		write_file("results", "\n")

# https://stackoverflow.com/questions/42970646/store-most-informative-features-from-nltk-naivebayesclassifier-in-a-list?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
def show_most_informative_features_in_list(classifier, n=10):
    """
    Return a nested list of the "most informative" features 
    used by the classifier along with it's predominant labels
    """
    cpdist = classifier._feature_probdist       # probability distribution for feature values given labels
    feature_list = []
    for (fname, fval) in classifier.most_informative_features(n):
        def labelprob(l):
            return cpdist[l, fname].prob(fval)
        labels = sorted([l for l in classifier._labels if fval in cpdist[l, fname].samples()], 
                        key=labelprob)
        feature_list.append([fname, labels[-1]])
    return feature_list

print(show_most_informative_features_in_list(classifier, 30))

save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

#classifier.show_most_informative_features()

print(str(counter_nt) + " counter notr" )
print(str(counter_neg) + " counter neg" )
print(str(counter_pos) + " counter pos" )
print(len(train))


end = time.time()
print(end - start)





