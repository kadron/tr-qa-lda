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
VERBOSE = False

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
    out = open("voc.pickle","wb")
    pickle.dump(VOCABULARY,out)
    out.close()
    wikifile.close()

def write_voc_as_dict_to_file(filename,voc_as_dict):
    with codecs.open(filename,'w+', 'utf-8') as v_file:
        v_file.write("First Line\n")
        for word,_ in voc_as_dict.items():
            v_file.write("%s\n" %word)

# voc_d2, voc2 = parse.load_vocabulary("../data/voc.pickle")
def load_vocabulary(voc_pickle):
    voc_as_dict = pickle.load(open(voc_pickle,'rb'))
    voc = ["FirstLine",]
    voc.extend(voc_as_dict.keys())
    return voc_as_dict, voc

# voc_d3, voc3 = parse.extend_vocabulary(questions,voc_d2)
def extend_vocabulary(lo_sents,voc_as_dict):
    length = len(voc_as_dict)
    for sent in lo_sents:
        words = word_tokenize(sent)
        for word in words:
            add_to_vocabulary(word, voc_as_dict = voc_as_dict)
    voc = ["FirstLine",]
    voc.extend(voc_as_dict.keys())
    print("Added %d words" %(len(voc_as_dict) - length) )
    return voc_as_dict, voc

def add_to_vocabulary_text(text):
    sentences = tokenizer.tokenize(text)
    for sent in sentences:
        words = word_tokenize(sent)
        for word in words:
            add_to_vocabulary(word)

def add_to_vocabulary(word,voc_as_dict=VOCABULARY):
    word =  word.lower()
    if word in STOPWORDS or word in tokenizer.PUNCTUATION:
        return
    if not word.isalnum():
        try:
            word = regexp_tokenizer.tokenize(word)[0]
        except IndexError:
            return
    if voc_as_dict.has_key(word):
        voc_as_dict[word] = voc_as_dict[word]+1
    else:
        voc_as_dict[word] = 1
        if VERBOSE:
            print("%s added" %word)

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
# questions = parse.write_questions("../data/questions.ldac",voc,q_ldac)
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
        word = word.lower()
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
            #print("word %s index:%s" %(word,index))
        except ValueError:
            if VERBOSE:
                print("%s is not found in vocabulary" %word)
    if len(temp) == 0:
        print(words)
        return
    line = ["%s " %len(temp),]
    for word,freq in temp.items():
        line.append("%s:%s " %(word,freq))
    ldac.append("".join(line))


def print_ldac(ldac_list,voc):
    for i in range(0,len(ldac_list)):
        items = ldac_list[i].split(" ")
        question = [items[0]+" ",]
        for freqs in items[1:]:
            if freqs:
		question.append(voc[int(freqs.split(":")[0])])
        print(str(i) + ": "+  ldac_list[i])
        print(str(i) +": "+ " ".join(question))
