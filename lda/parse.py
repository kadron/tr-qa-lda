import codecs
from nltk.corpus import stopwords
import nltk.data
from nltk.tokenize import PunktWordTokenizer
tokenizer = nltk.data.load('tokenizers/punkt/turkish.pickle')
punkt_word_tokenizer = PunktWordTokenizer()

STOPWORDS = stopwords.words('turkish')
VOCABULARY = {}

def main():
    wikifile = codecs.open("allDocsTogether","rU","utf-8")
    vocabulary = {}
    for i in range(0,5):
	title = wikifile.readline()
	print("Title: %s" %title)
	wikifile.readline()
	body = wikifile.readline()
	while body != u'\n':
		add_to_vocabulary_text(body)
		print(body)
		body = wikifile.readline()
    wikifile.close()

def add_to_vocabulary_text(text):
    sentences = tokenizer.tokenize(text)
    for sent in sentences:
        words = punkt_word_tokenizer.tokenize(sent)
        for word in words:
            add_to_vocabulary(word)

def add_to_vocabulary(word):
    word =  word.lowercase()
    if word in STOPWORDS or not word.isalnum():
        print(word)
        return
    if VOCABULARY.has_key(word):
        VOCABULARY[word] = VOCABULARY[word]+1
    else:
        VOCABULARY[word] = 1
