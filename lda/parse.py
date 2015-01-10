import codecs,pickle,traceback,sys
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

class vocabulary(object):
    def __init__(self,filename):
        self.vocabulary = {}
        self.voc_as_l = []
        if filename:
            self.voc_as_l = read_voc(filename)


def build_vocabulary():
    wikifile = codecs.open("allDocsTogether","rU","utf-8")
    #    for _ in range(0,COUNTER):
    while 1:
        title = wikifile.readline()
        if not title:
            break
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
        wikifile.readline()
        body = wikifile.readline()
        while body != u'\n':
            from_par_to_ldac(body)
            body = wikifile.readline()
    wikifile.close()
    out = open("corpus1.pickle","wb")
    pickle.dump(VOCABULARY,out)
    out.close()

def from_par_to_ldac(text):
    sentences = tokenizer.tokenize(text)
    for sent in sentences:
        words = word_tokenize(sent)
        from_sen_to_ldac(words,VOCABULARY_l,LDAC)

def read_voc(filename):
    with codecs.open(filename,"rU","utf-8") as voc_file:
        voc = voc_file.read().split('\n')
    return voc

def temp():
    while True:
        line = file.readline()
        if not line:
            break

def write_questions(filename,voc,ldac_q): # ../data/questions.ldac
    questions = []
    with codecs.open("trainingques.csv","rU","utf-8") as ques_file:
        while True:
            line = ques_file.readline()
            if not line:
                break
            question = line.split("\t")[1]
            words = word_tokenize(question)
            from_sen_to_ldac(words,voc,ldac_q)
            questions.append(question)
    with codecs.open(filename,'w+', 'utf-8') as v_file:
        v_file.write("\n".join(ldac_q))
    return questions

def from_sen_to_ldac(words,voc,ldac):
    temp = {}
    for word in words:
        if not word.isalnum():
            try:
                word = regexp_tokenizer.tokenize(word)[0]
            except IndexError:
                continue
        try:
            index = voc.index(word)
            if temp.has_key(index):
                temp[index] = temp[index] + 1
            else:
                temp[index] = 1
        except ValueError:
            pass
    if len(temp) == 0:
        print(words)
        return
    line = ["%s " %len(temp),]
    for word,freq in temp.items():
        line.append("%s:%s " %(word,freq))
    ldac.append("".join(line))
