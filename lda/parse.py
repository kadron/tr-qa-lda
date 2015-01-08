import codecs
from nltk.corpus import stopwords
import nltk.data
from nltk.tokenize import PunktWordTokenizer
tokenizer = nltk.data.load('tokenizers/punkt/turkish.pickle')
punkt_word_tokenizer = PunktWordTokenizer()

STOPWORDS = stopwords.words('turkish')
VOCABULARY = {}
VOCABULARY_l = []
LDAC= []

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
		body = wikifile.readline()
    wikifile.close()

def add_to_vocabulary_text(text):
    sentences = tokenizer.tokenize(text)
    for sent in sentences:
        words = punkt_word_tokenizer.tokenize(sent)
        for word in words:
            add_to_vocabulary(word)

def add_to_vocabulary(word):
    word =  word.lower()
    if word in STOPWORDS or not word.isalnum():
        print(word)
        return
    if VOCABULARY.has_key(word):
        VOCABULARY[word] = VOCABULARY[word]+1
    else:
        VOCABULARY[word] = 1

def to_ldac():
    voc = VOCABULARY.keys()
    docs = []
    wikifile = codecs.open("allDocsTogether","rU","utf-8")
    vocabulary = {}
    for i in range(0,5):
	title = wikifile.readline()
	print("Title: %s" %title)
	wikifile.readline()
	body = wikifile.readline()
	while body != u'\n':
		from_par_to_ldac(body,voc)
		body = wikifile.readline()
    wikifile.close()

def from_par_to_ldac(text,voc):
    sentences = tokenizer.tokenize(text)
    for sent in sentences:
        words = punkt_word_tokenizer.tokenize(sent)
        from_sen_to_ldac(words,voc)


def from_sen_to_ldac(words,voc):
    temp = {}
    for word in words:
            try:
                index = voc.index(word)
                if temp.has_key(index):
                    temp[index] = temp[index] + 1
                else:
                    temp[index] = 1
            except ValueError:
                pass
    line = ["[ %d " % len(temp),]
    for word,freq in temp:
        line.append("%s:%s " %(word,freq))
    line.append("]")
    print(line)
