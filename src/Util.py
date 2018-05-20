import re, pickle
import string #punctuation

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

def open_pickle(filename):
    infile = open(filename,'rb')
    opened_pickle = pickle.load(infile)
    infile.close()
    return opened_pickle

dict_stemmer = open_pickle("stemmer")
def stem_word(word):
	if word in dict_stemmer.keys():
		return dict_stemmer[word]
	else:
		return word

def add_to_freq_dict(dictionary, word):
	if word not in dictionary:
		freq = 1
		dictionary[word] = freq
	else:
		dictionary[word] += 1

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
	check_pos = re.findall(r'(?::\)|:-\)|=\)|:D|:d|<3|\(:|:\'\)|\^\^|;\)|\(-:)', word)
	check_neg = re.findall(r'(:-\(|:\(|;\(|;-\(|=\(|:/|:\\|-_-|\):|\)-:)', word)
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