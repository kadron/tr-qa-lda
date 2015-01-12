import os, sys, codecs
sys.path.append("/Users/cagil/work/HazirCevap/hazircevap2")
from search import indriDocFetch, indriHandler, queryBuilder

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

def find_related_docs():
    index = 1
    query_dir = "/home/cagil/tr-qa-lda/data/"
    doc_ids = indriHandler.singleIndriQuery("tr/lda_"+str(index))
    doc_dir = os.path.join(query_dir, "docs")

    for ind,doc_id in enumerate(doc_ids):
        doc = indriDocFetch.getDocTr(doc_id)
        doc_decoded = doc.decode('utf-8')
        with codecs.open(os.path.join(doc_dir, "lda_"+str(index)+"_"+str(ind)),'w+', 'utf-8') as q_file:
            q_file.write(doc_decoded)
