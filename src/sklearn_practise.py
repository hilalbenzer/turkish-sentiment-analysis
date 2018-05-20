import numpy as np
import time
import Util
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.pipeline import Pipeline

from sklearn import metrics

from pathlib import Path

from spell_correction import correction

src_folder = Path("./")
stopwords = Util.read_file(Path(src_folder / "stopwords.txt")).split("\n")

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
	return(sentence)

start = time.time()
data = Util.open_pickle("dataTrain")
labels = Util.open_pickle("labelsTrain")

categories = ['neg', 'notr', 'pos']

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])
text_clf.fit(data, labels)

docs_test = Util.open_pickle("dataTest")
labels = Util.open_pickle("labelsTest")
#docs_test = data
#docs_test = [preprocess(sen) for sen in docs_test ]
predicted = text_clf.predict(docs_test)
print(np.mean(predicted == labels))

print(metrics.classification_report(labels, predicted,
     target_names=categories))

print(metrics.confusion_matrix(labels, predicted))

docs_test = Util.read_file("test_tweets").split("\n")
docs_test_processed = [preprocess(sen.lower()) for sen in docs_test ]
predicted = text_clf.predict(docs_test_processed)

count = 0
for p in predicted:
	print("Sentence: " + docs_test[count])
	print("Predicted: " + categories[p])
	count += 1

end = time.time()
print("Elapsed time: " + str(end - start))
