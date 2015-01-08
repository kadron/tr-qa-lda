import codecs,pickle
from nltk.corpus import stopwords
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/turkish.pickle')
from nltk.tokenize import word_tokenize
# alternative word tokenizer
#from nltk.tokenize import PunktWordTokenizer
#punkt_word_tokenizer = PunktWordTokenizer()

from nltk.tokenize import RegexpTokenizer
regexp_tokenizer = RegexpTokenizer(r'\w+')

COUNTER = 5
STOPWORDS = stopwords.words('turkish')
VOCABULARY = {}
VOCABULARY_l = []
LDAC= []

def main():
    wikifile = codecs.open("allDocsTogether","rU","utf-8")
    for _ in range(0,COUNTER):
        title = wikifile.readline()
        print("Title: %s" %title)
        wikifile.readline()
        body = wikifile.readline()
        while body != u'\n':
            add_to_vocabulary_text(body)
            body = wikifile.readline()
    out = open("voc1.pickle","wb")
    pickle.dump(VOCABULARY,out)
    out.close()
    wikifile.close()

def add_to_vocabulary_text(text):
    sentences = tokenizer.tokenize(text)
    for sent in sentences:
        words = word_tokenize(sent)
        for word in words:
            add_to_vocabulary(word)

def add_to_vocabulary(word):
    word =  word.lower()
    if word in STOPWORDS or word in tokenizer.PUNCTUATION:
        print(word)
        return
    if not word.isalnum():
        try:
            word = regexp_tokenizer.tokenize(word)[0]
        except IndexError:
            return
    if VOCABULARY.has_key(word):
        VOCABULARY[word] = VOCABULARY[word]+1
    else:
        VOCABULARY[word] = 1

def to_ldac():
    voc = VOCABULARY.keys()
    VOCABULARY_l.extend(VOCABULARY.keys())
    wikifile = codecs.open("allDocsTogether","rU","utf-8")
    for _ in range(0,COUNTER):
        title = wikifile.readline()
        print("Title: %s" %title)
        wikifile.readline()
        body = wikifile.readline()
        while body != u'\n':
            from_par_to_ldac(body,voc)
            body = wikifile.readline()
    wikifile.close()
    out = open("corpus1.pickle","wb")
    pickle.dump(VOCABULARY,out)
    out.close()

def from_par_to_ldac(text,voc):
    sentences = tokenizer.tokenize(text)
    for sent in sentences:
        words = word_tokenize(sent)
        from_sen_to_ldac(words,voc)

def from_sen_to_ldac(words,voc):
    temp = {}
    for word in words:
        if not word.isalnum():
            try:
                word = regexp_tokenizer.tokenize(word)[0]
            except IndexError:
                continue
        try:
            index = VOCABULARY_l.index(word) + 1
            if temp.has_key(index):
                temp[index] = temp[index] + 1
            else:
                temp[index] = 1
        except ValueError:
            pass
    line = ["[ %d " % len(temp),]
    for word,freq in temp.items():
        line.append("%s:%s " %(word,freq))
    line.append("]")
    LDAC.append("".join(line))
