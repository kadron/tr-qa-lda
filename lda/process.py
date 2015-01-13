from __future__ import absolute_import, unicode_literals  # noqa

import os, math, codecs
import numpy as np

from subprocess import call

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



#Information Retrieval metric, p&q are tuples
def ir(p,q,num_topics):
	#kl_div(p,(p+q)/2)+kl_div(q,(p+q)/2)
	containsList = [False] * num_topics
	for tp in p:
		for i in xrange(num_topics):
			if tp[0]==i:
				containsList[i] = True
	for i,b in enumerate(containsList):
		if(b==False):
			p.append((i,0))

	containsList = [False] * num_topics
	for tq in q:
		for i in xrange(num_topics):
			if tq[0]==i:
				containsList[i] = True
	for i,b in enumerate(containsList):
		if(b==False):
			q.append((i,0))

	total=0
	for tp in p:
		for tq in q:
			for i in xrange(num_topics):
				if tp[0]==i and tq[0]==i and (tp[1]!=0 or tq[1]!=0):
					x1 = 0
					x2 = 0
					if tp[1]!=0:
						x1 = tp[1]*math.log(abs((2*tp[1])/(tp[1]+tq[1])))
					if tq[1]!=0:
						x2 = tq[1]*math.log(abs((2*tq[1])/(tp[1]+tq[1])))
					total = total + x1 + x2
					break
	return total
def w(p,q,num_topics):
	return 10**(-ir(p,q,num_topics));

"""
#Topic-Word Distribution Metric
def sim1(p,q,num_topics):
	total = 0;
	for i in xrange(num_topics):
		total = total + w(p[i],q[i])
	return total/num_topics
"""

#Document-Topic Distribution Metric
def sim2(p,q,num_topics):
	return w(p,q,num_topics)

def compare_sq(dist_list,num_question,num_answer,num_topics):
	#50985 answers to each question
	answer_list = []
	metric_list = []

	for q in dist_list[-num_question:]:
		max_answer = [-1]*50
		max_metric = [-1]*50

		for i,p in enumerate(dist_list[0:num_answer]):
			metric = sim2(p,q,num_topics)
			num_s = 50
			for j in xrange(num_s):
				if j == 0:
					if metric > max_metric[0]:
						max_metric = [metric] + max_metric[1:num_s]
						max_answer = [i] + max_answer[1:num_s]
						break
				elif j == num_s-1:
					if metric > max_metric[num_s-1]:
						max_metric = max_metric[0:num_s-1] + [metric]
						max_answer = max_answer[0:num_s-1] + [i]
						break
				else:
					if metric > max_metric[j]:
						max_metric = max_metric[0:j] + [metric] + max_metric[j+1:num_s]
						max_answer = max_answer[0:j] + [i] + max_answer[j+1:num_s]
						break

		answer_list.append(max_answer)
		metric_list.append(max_metric)

	return answer_list,metric_list

def main():
	#Loads dataset and vocabulary
	#Generating topics and distributions
	print('Starting up!')
	num_topics = 10
	num_question = 50
	num_answer = 50985
	corpus_name = '../data/ldac/deriv/sq50.txt'
	voc_name = '../data/voc/deriv/all.txt'
	corpus = corpora.BleiCorpus(corpus_name,voc_name)
	print('Corpus processed!')
	#id2word = corpora.Dictionary.load('../data/voc_2.txt')
	lda = models.ldamodel.LdaModel(corpus, num_topics=num_topics, chunksize=2000, decay=0.5, offset=1.0, passes=1, update_every=0, eval_every=10, iterations=20000, gamma_threshold=0.001)
	print('LDA applied to corpus!')

	#print('=== Topic-Word Distributions ===')
	#topic_word_list = lda.show_topics()

	#for i in xrange(num_topics):
	#	print('Topic {} : {}'.format(i,' '.join(topic_word_list[i][0:])))

	print ('=== Document-Topic Distributions ===')
	#Writing doc_topic distributions to a file to parse later
	#doc_topic = lda[corpus]
	dist_list = list(lda[corpus])
	answer_list,metric_list = compare_sq(dist_list,num_question,num_answer,num_topics)

	print('Answers compared!')
	answer_list
	f = open('{}{}'.format(corpus_name,'.answers'), 'w')

	print('Answers for each question.')
	for i,answers in enumerate(answer_list):
		answers
		f.write('Question {}: '.format(i))
		for j in xrange(50):
			f.write('{} '.format(answers[j]))
		f.write('\n')
	f.close()
	print('Results written !')

if __name__ == '__main__':
	main()
