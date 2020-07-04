# Here, we take the annotated articles as input, split them into sentences and identify the sentences that contain at least 1 negative sentiment words
# We extend this code from a sentence-level to a document-level. We thus check the number of negative sentiment words present in each document.

# NOTE: There is a separate MSThesisWork folder under Documents, which contains the data resources of our recommendation task

# Reading packages
import pandas as pd
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
stopword_list = list(set(stopwords.words('english')))

# Reading the input files
nrc_neg_words_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/BiuNegativeWords.csv'
nrc_neg_words = pd.read_csv(nrc_neg_words_readpath)
nrc_neg_word_list = list(nrc_neg_words['neg_words'])

anno_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/recoFinalcleanData19thAugust.csv'
anno_data = pd.read_csv(anno_data_readpath)

neg_sent_anno_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/recoDataNegDocuments_22ndAugust.csv'

# Index at 0 : X.AUTHID, 1: spec_domain, 2: clean.content

row_id_list = list()
doc_neg_count_list = list()
neg_words_coll_list = list()

# Here, we also implement the negated context code. Make the same change at a document- and sentence-level
for row_id in range(anno_data.shape[0]):
    clean_words = word_tokenize(anno_data.iloc[row_id, 2])
    # Removing the stopwords
    clean_words1 = [word for word in clean_words if word not in stopword_list]
    num_neg_words = 0
    neg_words_list = list()
    for word in clean_words:
        for neg_word in nrc_neg_word_list:
            if neg_word == word:
                # This indicates that a negative word is present in this sentence. We add it to the negative sentences list.
                neg_words_list.append(word)
                num_neg_words +=1

    row_id_list.append(anno_data.iloc[row_id, 0])
    doc_neg_count_list.append(num_neg_words)
    neg_words_coll_list.append(neg_words_list)

    if row_id % 10 ==0:
        print(row_id)

# Exporting to a csv file
neg_docs_data = pd.DataFrame({'X.AUTHID': row_id_list, 'neg_words_of_doc': neg_words_coll_list, 'neg_words': neg_words_coll_list})
neg_docs_data.to_csv(neg_sent_anno_data_writepath, sep='|')

# These identified sentences will be particularly be manually annotated. For the remaining 14 items, we randomly select them, and may be from multiple companies



