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
    all_sentences = []
    for doc_id in range(0,5):
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
                    for sent_raw in sentences:
                        sent = sent_raw.strip().strip(".").lower()
                        if sent:
                            all_sentences.append(sent)
    all_related_text = "\n".join(all_sentences)
    if all_related_text.find(answer) > -1:
        with codecs.open("../data/answers/"+str(index),'w+', 'utf-8') as docs_file:
            docs_file.write(all_related_text)
    else:
        print(index,answer)
    return all_sentences


def merge_and_write_answers(n=range(1,357)):
    with codecs.open("../data/last_questions_answers.txt","rU","utf-8") as ans_file:
        for index in n:
            answer = ans_file.readline()
            _ = merge_and_write_answers_inner(index,answer.strip().lower())
