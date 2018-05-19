import re, os
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
import string #punctuation
from TurkishStemmer import TurkishStemmer
import time
import operator #for sorting dict
import pickle

WORDS = dict()
def words(text): return re.findall(r'\w+', text.lower())
with open("big.txt", "r", encoding = 'utf-8') as f:
    for line in f:
        splitted = line.split()
        WORDS[splitted[0]] = int(splitted[1])
#WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    if  word in WORDS.keys():
        number = WORDS[word]
    else:
        number = 1
    if number == 0:
        number = 1
    return number / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcçdefgğhıijklmnoöprsştuüvyzw'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
def print_diff(word, s):
    if not word == s:
        print(word + " --> " + s)



def read_file(filename):
	f = open(filename, "r", encoding="utf-8")
	file_text = f.read()
	f.close()
	return file_text

def write_file(filename, output):
	full_filename = './' + filename + '.txt'
	file = open(full_filename, 'w', encoding = "utf-8")
	file.write(str(output))
	file.close()

def add_to_freq_dict(dictionary, word):
	if word not in dictionary:
		freq = 1
		dictionary[word] = freq
	else:
		dictionary[word] += 1

stemmer = TurkishStemmer()
stopwords = read_file("..\\stopwords_new.txt").split("\n")
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
	word_list = [ replace_turkish_char(stemmer.stem(correction(remove_punct(remove_with_regex(word))))) for word in word_list ]
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

direct = ".\\Train\\"

print("Reading files...")
positive_raw = read_file(os.path.join(direct, "positive-train"))
negative_raw = read_file(os.path.join(direct, "negative-train"))
notr_raw = read_file(os.path.join(direct, "notr-train"))

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
print("This thing...")
def create_pickle(filename, output):
    outfile = open(filename,'wb')
    pickle.dump(output,outfile)
    outfile.close()

create_pickle("data", data)
create_pickle("labels", labels)

end = time.time()
print(end - start)
