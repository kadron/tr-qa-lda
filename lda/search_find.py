import os, sys, codecs
sys.path.append("/Users/cagil/work/HazirCevap/hazircevap2")
sys.path.append("/home/hazircevap/hazircevap")
from search import indriDocFetch, indriHandler, queryBuilder
from nltk import word_tokenize, sent_tokenize

def prepare_param_files():
    index = 1
    queryBuilder.queryDir = "./"
    queryBuilder.indexDir = queryBuilder.index_dir_tr
    with codecs.open("../data/last_questions.txt","rU","utf-8") as ques_file:
        while True:
            line = ques_file.readline()
            if not line:
                break
            queryBuilder.buildIndriQuerySingleFromQuestion("queries/tr/lda_"+str(index), line.strip("\n"))
            index += 1

def find_related_docs(index):
    query_dir = "/home/cagil/tr-qa-lda/data/"
    doc_ids = indriHandler.singleIndriQuery("tr/lda_"+str(index))
    doc_dir = os.path.join(query_dir, "docs")

    for ind,doc_id in enumerate(doc_ids):
        doc = indriDocFetch.getDocTr(doc_id)
        doc_decoded = doc.decode('utf-8')
        with codecs.open(os.path.join(doc_dir, "lda_"+str(index)+"_"+str(ind)),'w+', 'utf-8') as q_file:
            q_file.write(doc_decoded)

def find_related_docs_all(n=range(1,357)):
    for index in n:
        find_related_docs(index)

def merge_and_write_answers_inner(index,answer):
    for doc_id in range(0,5):
        all_sentences = []
        doc_filename = "../data/docs/lda_"+str(index)+"_"+str(doc_id)
        if os.path.exists(doc_filename):
            with codecs.open(doc_filename,"rU","utf-8") as doc_file:
                line = doc_file.readline()
                while(line != "\n"):
                    line = doc_file.readline()
                while True:
                    if not line:
                        break
                    line = doc_file.readline()
                    sentences = sent_tokenize(line)
                    for sent in sentences:
                        all_sentences.append(sent.strip().strip("."))
    all_related_text = "\n".join(all_sentences)
    if all_related_text.find(answer) > -1:
        with codecs.open("../data/answers/index",'w+', 'utf-8') as docs_file:
            docs_file.write(all_related_text)
    else:
        print(index)
    return all_related_text



def merge_and_write_answers(n=range(1,357)):
    with codecs.open("../data/last_questions_answers.txt","rU","utf-8") as ans_file:
        for index in n:
            answer = ans_file.readline()
            merge_and_write_answers_inner(index,answer.strip())
