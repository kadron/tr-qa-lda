from __future__ import absolute_import, unicode_literals  # noqa

import os

import numpy as np
import math
import codecs

import lda
import lda.utils

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
	_test_dir = os.path.join(os.path.dirname(__file__), '../data')
	X1 = load_dataset(_test_dir,'corpus56100.ldac.txt')
	Q1 = load_dataset(_test_dir,'questions3.ldac')
	vocab = load_vocab(_test_dir,'voc_2.txt')

	X1.shape
	Q1.shape
	vocab.shape

	#Generating topics and distributions
	model = lda.LDA(n_topics=20, n_iter=1000, random_state=1)
	model.fit(X)
	
	topic_word = model.topic_word_
	n_top_words = 8

	for i,topic_dist in enumerate(topic_word):
		topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
		topic_str = ' '.join(topic_words)
		print('Topic {}: {}'.format(i, topic_str))

	doc_topic = model.doc_topic_
	print(doc_topic.shape)

if __name__ == '__main__':
	main()