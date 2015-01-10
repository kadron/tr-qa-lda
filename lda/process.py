from __future__ import absolute_import, unicode_literals  # noqa

import os

import numpy as np

import lda
import lda.utils

def load_dataset(folder, filename):
	ldac_fn = os.path.join(folder, filename)
	return lda.utils.ldac2dtm(open(ldac_fn), offset=0)

def load_vocab(folder, filename):
	vocab_fn = os.path.join(folder, filename)
	with open(vocab_fn) as f:
		vocab = tuple(f.read().split())
	return vocab

def main():
	#Loads dataset and vocabulary
	_test_dir = os.path.join(os.path.dirname(__file__), '../data')
	X = load_dataset(_test_dir,'text_1.ldac.txt')
	vocab = load_vocab(_test_dir,'voc_1.txt')

	#Generating topics and distributions
	model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
	model.fit(X)
	
	topic_word = model.topic_word_
	n_top_words = 8
	print(type(vocab[0]))
	print(type(vocab[1]))
	print(type(vocab[2]))
	print(type(vocab[3]))

	for i,topic_dist in enumerate(topic_word):
		topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
		topic_str = ' '.join(topic_words)
		print('Topic {}: {}'.format(i, topic_str))


if __name__ == '__main__':
	main()