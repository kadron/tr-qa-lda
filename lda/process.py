from __future__ import absolute_import, unicode_literals  # noqa

import os, math, codecs
import numpy as np

from gensim import corpora
from gensim import models

def load_dataset(folder, filename):
	ldac_fn = os.path.join(folder, filename)
	return lda.utils.ldac2dtm(open(ldac_fn), offset=0)

def load_vocab(folder, filename):
	vocab_fn = os.path.join(folder, filename)
	with codecs.open(vocab_fn,'r','UTF-8') as f:
		vocab = tuple(f.read().split())
	return vocab

#Discrete KL Divergence, p&q are tuples
def kl_div(p,q):
	total = 0;
	for i in xrange(len(p)):
		total = total + p[i]*math.log(p[i]/q[i])
	return total

#Information Retrieval metric, p&q are tuples
def ir(p,q):
	return kl_div(p,(p+q)/2)+kl_div(q,(p+q)/2)

def w(p,q):
	return 10**(-ir(p,q));

def sim1(p,q,num_topics):
	total = 0;
	for i in xrange(num_topics):
		total = total + w(p[i],q[i])
	return total/num_topics

def sim2(p,q):
	return w(p,q)

def main():
	#Loads dataset and vocabulary
	#Generating topics and distributions
	num_topics = 20

	corpus = corpora.BleiCorpus('../data/totalcorpus.ldac','../data/voc_2.txt')
	#id2word = corpora.Dictionary.load('../data/voc_2.txt')
	lda = models.ldamodel.LdaModel(corpus, num_topics=num_topics, chunksize=2000, decay=0.5, offset=1.0, passes=5, update_every=0, eval_every=10, iterations=20000, gamma_threshold=0.001)
	#print('Corpus1 finished!')

	

	#print('=== Topic-Word Distributions ===')
	#topic_word_list = lda.show_topics()
 
	#for i in xrange(num_topics):
	#	print('Topic {} : {}'.format(i,' '.join(topic_word_list[i][0:])))

	#print ('=== Document-Topic Distributions ===')
	doc_topic = lda[corpus]
	for doc in doc_topic:
		print(doc)





if __name__ == '__main__':
	main()