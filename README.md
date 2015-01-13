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

voc_org = parse.build_vocabulary_from_sent_file("../data/answers/all.txt","../data/voc/org/all.txt")

voc_org_list = parse.read_voc("../data/voc/org/all.txt")

parse.sentence_file_to_ldac("../data/last_questions.txt","../data/ldac/org/last_questions.txt", voc_org_list)

parse.sentence_file_to_ldac("../data/answers/all.txt","../data/ldac/org/all.txt", voc_org_list)

----

big_voc_new = parse.build_vocabulary_from_sent_file("../data/stemmed/deriv/all.txt","../data/voc/deriv/all.txt")

big_voc_new_list = parse.read_voc("../data/voc/deriv/all.txt")

parse.sentence_file_to_ldac("../data/stemmed/deriv/last_questions.txt","../data/ldac/deriv/last_questions.txt", big_voc_new_list)

parse.sentence_file_to_ldac("../data/stemmed/deriv/all.txt","../data/ldac/deriv/all.txt", big_voc_new_list)

To test:

parse.print_ldac_from_file("../data/ldac/org/last_questions.txt", voc_org_list)

parse.print_ldac_from_file("../data/ldac/deriv/last_questions.txt",big_voc_new_list)