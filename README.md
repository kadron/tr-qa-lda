# tr-qa-lda
LDA Implementation for QA Matching on Turkish corpus

Vocabulary oluşturma örnek:

small_voc = parse.build_vocabulary_from_sent_file("../data/stemmed/deriv/last_questions.txt","/tmp/voc/deriv/last_questions.txt")

big_voc = parse.build_vocabulary_from_sent_file("../data/stemmed/deriv/all.txt","/tmp/voc/deriv/all.txt")

LDAC dosyası oluşturma (sent_file'dan):

parse.sentence_file_to_ldac("../data/stemmed/deriv/last_questions.txt","/tmp/ldac/deriv/last_questions.txt", small_voc.keys())

parse.sentence_file_to_ldac("../data/stemmed/deriv/last_questions.txt","/tmp/ldac/deriv/last_questions.txt", big_voc.keys())

parse.sentence_file_to_ldac("../data/stemmed/deriv/all.txt","/tmp/ldac/deriv/all.txt", big_voc.keys())

REALTIME

big_voc_new = parse.build_vocabulary_from_sent_file("../data/stemmed/deriv/all.txt","../data/voc/deriv/all.txt")

big_voc_new_list = read_voc("../data/voc/deriv/all.txt")

parse.sentence_file_to_ldac("../data/stemmed/deriv/last_questions.txt","../data/ldac/deriv/last_questions.txt", big_voc_new_list)

parse.sentence_file_to_ldac("../data/stemmed/deriv/all.txt","../data/ldac/deriv/all.txt", big_voc_new_list)
