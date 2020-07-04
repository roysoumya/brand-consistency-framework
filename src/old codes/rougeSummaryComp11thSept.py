# Here we compute the ROUGE-1 and ROUGE-2
# Here, we have to first process the 3 sentences. Not adjacent -- form unigrams and bigrams -- compute ROUGE-N precision, ROUGE-N recall
# ROUGE-N  f1 score
# Also compute the ROUGE-L score

# Run this code using Python 2.7, otherwise the string.translate() does not work

from PyRouge.pyrouge import Rouge
import pandas as pd
from nltk import word_tokenize
from nltk.util import ngrams
import string

import math

# Computing ROUGE-L precision, recall and F1 score
r_summ_evaluate = Rouge()

# Trying with a sample summary
# system_generated_summary = " The Kyrgyz President pushed through the law requiring the use of ink during the upcoming Parliamentary and Presidential elections In an effort to live up to its reputation in the 1990s as an island of democracy. The use of ink is one part of a general effort to show commitment towards more open elections. improper use of this type of ink can cause additional problems as the elections in Afghanistan showed. The use of ink and readers by itself is not a panacea for election ills."
# manual_summmary = " The use of invisible ink and ultraviolet readers in the elections of the Kyrgyz Republic which is a small, mountainous state of the former Soviet republic, causing both worries and guarded optimism among different sectors of the population. Though the actual technology behind the ink is not complicated, the presence of ultraviolet light (of the kind used to verify money) causes the ink to glow with a neon yellow light. But, this use of the new technology has caused a lot of problems. "

# print(r_summ_evaluate.rouge_l([system_generated_summary], [manual_summmary]))

# Here we read the file which mentions the 3 sentences for each technique, in three adjacent columns
#summ_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/GoldDataOnly36_12thSept.csv'
# 1 : X.AUTHID, 2 : spec_domain, 3: site.content  4-6: GOLD, 7-9 : LEAD, 10-12 : RAND, 13-15 : INCONST, 16-18 : INCONST_NEG, 19-21 : HYBRID1

#summ_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/GoldDataAllAspectsWithHybrid_13thSept.csv'
# 1 : X.AUTHID, 2 : spec_domain, 3: site.content  4-6: GOLD, 7-9: LEAD, 10-12: Hybrid, 13-15: Incons, 16-18: Neg, 19-21: Ctr, 22-24: InconsNeg
summ_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/GoldDataAllAspects_Annotate_Partial_17thSept.csv'

summ_data = pd.read_csv(summ_data_readpath)
summ_data = summ_data.fillna("")


#
def rouge_one(own_summ, gold_summ):
    # Lets go with unique words only and no preprocessing. But still look into it.
    own_unigrams = set(own_summ)
    gold_unigrams = set(gold_summ)

    ovlp_words = own_unigrams.intersection(gold_unigrams)
    # print(ovlp_words)

    if len(own_unigrams) > 0:
        prec = len(ovlp_words) * 1.0 / len(own_unigrams)
    else:
        prec = 0.0

    if len(gold_unigrams) > 0:
        rec = len(ovlp_words) * 1.0 / len(gold_unigrams)
    else:
        rec = 0.0
    if prec == 0.0 and rec == 0.0:
        fscore = 0.0
    else:
        fscore = (2.0 * prec * rec) / (prec + rec)
    return fscore


article1 = "The sun rises in the east and sets in the west. Today I felt really alive and the sound of the morning train made fall in love with my beloved home ever again."

# Here we evaluate our generated 3 sentences with the Gold standard sentences
# For ROUGE-1
# rouge_one(article1, article1)

# For ROUGE-2
# rouge_N(article1, article1, 2)

# For ROUGE-L
# r_summ_evaluate.rouge_l([article1], [article1])
#rouge1_rand_list = list()
rouge1_lead_list = list()
rouge1_hybrid1_list = list()
rouge1_inconst_list = list()
rouge1_neg_list = list()
rouge1_ctr_list = list()
rouge1_inconst_neg_list = list()


#rouge2_rand_list = list()
rouge2_lead_list = list()
rouge2_hybrid1_list = list()
rouge2_inconst_list = list()
rouge2_neg_list = list()
rouge2_ctr_list = list()
rouge2_inconst_neg_list = list()


#rouge_lcs_rand_list = list()
rouge_lcs_lead_list = list()
rouge_lcs_hybrid1_list = list()
rouge_lcs_inconst_list = list()
rouge_lcs_neg_list = list()
rouge_lcs_ctr_list = list()
rouge_lcs_inconst_neg_list = list()


#table = string.maketrans("", "")
# 1 : X.AUTHID, 2 : spec_domain, 3: site.content  4-6: GOLD, 7-9: LEAD, 10-12: Hybrid, 13-15: Incons, 16-18: Neg, 19-21: Ctr, 22-24: InconsNeg
# We have GOLD-3 data for only 36 web articles
for row_ind in range(summ_data.shape[0]):
    gold1_tokens = word_tokenize((summ_data.iloc[row_ind, 3]).translate(None, string.punctuation))
    gold2_tokens = word_tokenize((summ_data.iloc[row_ind, 4]).translate(None, string.punctuation))
    gold3_tokens = word_tokenize((summ_data.iloc[row_ind, 5]).translate(None, string.punctuation))

    lead1_tokens = word_tokenize((summ_data.iloc[row_ind, 6]).translate(None, string.punctuation))
    lead2_tokens = word_tokenize((summ_data.iloc[row_ind, 7]).translate(None, string.punctuation))
    lead3_tokens = word_tokenize((summ_data.iloc[row_ind, 8]).translate(None, string.punctuation))

    hybrid1_tokens = word_tokenize((summ_data.iloc[row_ind, 9]).translate(None, string.punctuation))
    hybrid2_tokens = word_tokenize((summ_data.iloc[row_ind, 10]).translate(None, string.punctuation))
    hybrid3_tokens = word_tokenize((summ_data.iloc[row_ind, 11]).translate(None, string.punctuation))

    inconst1_tokens = word_tokenize((summ_data.iloc[row_ind, 12]).translate(None, string.punctuation))
    inconst2_tokens = word_tokenize((summ_data.iloc[row_ind, 13]).translate(None, string.punctuation))
    inconst3_tokens = word_tokenize((summ_data.iloc[row_ind, 14]).translate(None, string.punctuation))

    neg1_tokens = word_tokenize((summ_data.iloc[row_ind, 15]).translate(None, string.punctuation))
    neg2_tokens = word_tokenize((summ_data.iloc[row_ind, 16]).translate(None, string.punctuation))
    neg3_tokens = word_tokenize((summ_data.iloc[row_ind, 17]).translate(None, string.punctuation))

    ctr1_tokens = word_tokenize((summ_data.iloc[row_ind, 18]).translate(None, string.punctuation))
    ctr2_tokens = word_tokenize((summ_data.iloc[row_ind, 19]).translate(None, string.punctuation))
    ctr3_tokens = word_tokenize((summ_data.iloc[row_ind, 20]).translate(None, string.punctuation))

    inconst_neg1_tokens = word_tokenize((summ_data.iloc[row_ind, 21]).translate(None, string.punctuation))
    inconst_neg2_tokens = word_tokenize((summ_data.iloc[row_ind, 22]).translate(None, string.punctuation))
    inconst_neg3_tokens = word_tokenize((summ_data.iloc[row_ind, 23]).translate(None, string.punctuation))


    gold_side_1 = gold1_tokens + gold2_tokens + gold3_tokens
    #rand_side_1 = rand1_tokens + rand2_tokens + rand3_tokens
    hybrid_side_1 = hybrid1_tokens + hybrid2_tokens + hybrid3_tokens
    lead_side_1 = lead1_tokens + lead2_tokens + lead3_tokens
    inconst_side_1 = inconst1_tokens + inconst2_tokens + inconst3_tokens
    neg_side_1 = neg1_tokens + neg2_tokens + neg3_tokens
    ctr_side_1 = ctr1_tokens + ctr2_tokens + ctr3_tokens
    inc_neg_side_1 = inconst_neg1_tokens + inconst_neg2_tokens + inconst_neg3_tokens


    #rouge1_rand_list.append(rouge_one(rand_side_1, gold_side_1))
    rouge1_lead_list.append(rouge_one(lead_side_1, gold_side_1))
    rouge1_hybrid1_list.append(rouge_one(hybrid_side_1, gold_side_1))
    rouge1_inconst_list.append(rouge_one(inconst_side_1, gold_side_1))
    rouge1_neg_list.append(rouge_one(neg_side_1, gold_side_1))
    rouge1_ctr_list.append(rouge_one(ctr_side_1, gold_side_1))
    rouge1_inconst_neg_list.append(rouge_one(inc_neg_side_1, gold_side_1))


    gold_side_2 = list(ngrams(gold1_tokens, 2)) + list(ngrams(gold2_tokens, 2)) + list(ngrams(gold3_tokens, 2))
    #rand_side_2 = list(ngrams(rand1_tokens, 2)) + list(ngrams(rand2_tokens, 2)) + list(ngrams(rand3_tokens, 2))
    hybrid_side_2 = list(ngrams(hybrid1_tokens, 2)) + list(ngrams(hybrid2_tokens, 2)) + list(
        ngrams(hybrid3_tokens, 2))
    lead_side_2 = list(ngrams(lead1_tokens, 2)) + list(ngrams(lead2_tokens, 2)) + list(ngrams(lead3_tokens, 2))
    inconst_side_2 = list(ngrams(inconst1_tokens, 2)) + list(ngrams(inconst2_tokens, 2)) + list(
        ngrams(inconst3_tokens, 2))
    neg_side_2 = list(ngrams(neg1_tokens, 2)) + list(ngrams(neg2_tokens, 2)) + list(
        ngrams(neg3_tokens, 2))
    ctr_side_2 = list(ngrams(ctr1_tokens, 2)) + list(ngrams(ctr2_tokens, 2)) + list(
        ngrams(ctr3_tokens, 2))
    inc_neg_side_2 = list(ngrams(inconst_neg1_tokens, 2)) + list(ngrams(inconst_neg2_tokens, 2)) + list(
        ngrams(inconst_neg3_tokens, 2))


    #rouge2_rand_list.append(rouge_one(rand_side_2, gold_side_2))
    rouge2_lead_list.append(rouge_one(lead_side_2, gold_side_2))
    rouge2_hybrid1_list.append(rouge_one(hybrid_side_2, gold_side_2))
    rouge2_inconst_list.append(rouge_one(inconst_side_2, gold_side_2))
    rouge2_neg_list.append(rouge_one(neg_side_2, gold_side_2))
    rouge2_ctr_list.append(rouge_one(ctr_side_2, gold_side_2))
    rouge2_inconst_neg_list.append(rouge_one(inc_neg_side_2, gold_side_2))
    # 1 : X.AUTHID, 2 : spec_domain, 3: site.content  4-6: GOLD, 7-9: LEAD, 10-12: Hybrid, 13-15: Incons, 16-18: Neg, 19-21: Ctr, 22-24: InconsNeg

    rouge_lcs_lead_list.append(
        r_summ_evaluate.rouge_l(" ".join(summ_data.iloc[row_ind, 3:6]), " ".join(summ_data.iloc[row_ind, 6:9])))
    rouge_lcs_hybrid1_list.append(r_summ_evaluate.rouge_l(" ".join(summ_data.iloc[row_ind, 3:6]),
                                                          " ".join(summ_data.iloc[row_ind, 9:12])))
    #rouge_lcs_rand_list.append(r_summ_evaluate.rouge_l(" ".join(summ_data.iloc[row_ind, 3:6]), " ".join(summ_data.iloc[row_ind, 9:12])))
    rouge_lcs_inconst_list.append(r_summ_evaluate.rouge_l(" ".join(summ_data.iloc[row_ind, 3:6]),
                                                          " ".join(summ_data.iloc[row_ind, 12:15])))
    rouge_lcs_neg_list.append(r_summ_evaluate.rouge_l(" ".join(summ_data.iloc[row_ind, 3:6]),
                                                          " ".join(summ_data.iloc[row_ind, 15:18])))
    rouge_lcs_ctr_list.append(r_summ_evaluate.rouge_l(" ".join(summ_data.iloc[row_ind, 3:6]),
                                                          " ".join(summ_data.iloc[row_ind, 18:21])))
    rouge_lcs_inconst_neg_list.append(r_summ_evaluate.rouge_l(" ".join(summ_data.iloc[row_ind, 3:6]),
                                                              " ".join(summ_data.iloc[row_ind, 21:24])))


import numpy as np

print('ROUGE-1 scores')
#print('Random : ', np.mean(rouge1_rand_list))
print('Hybrid : ', np.mean(rouge1_hybrid1_list))
print('Lead : ', np.mean(rouge1_lead_list))
print('Inconst : ', np.mean(rouge1_inconst_list))
print('Neg : ', np.mean(rouge1_neg_list))
print('Centrality : ', np.mean(rouge1_ctr_list))
print('Inconst Neg : ', np.mean(rouge1_inconst_neg_list))


print('ROUGE-2 scores')
#print('Random : ', np.mean(rouge2_rand_list))
print('Hybrid : ', np.mean(rouge2_hybrid1_list))
print('Lead : ', np.mean(rouge2_lead_list))
print('Inconst : ', np.mean(rouge2_inconst_list))
print('Neg : ', np.mean(rouge2_neg_list))
print('Centrality : ', np.mean(rouge2_ctr_list))
print('Inconst Neg : ', np.mean(rouge2_inconst_neg_list))


print("ROUGE-LCS scores")
#print('Random : ', np.mean(rouge_lcs_rand_list))
print('Hybrid : ', np.mean(rouge_lcs_hybrid1_list))
print('Lead : ', np.mean(rouge_lcs_lead_list))
print('Inconst : ', np.mean(rouge_lcs_inconst_list))
print('Neg : ', np.mean(rouge_lcs_neg_list))
print('Centrality : ', np.mean(rouge_lcs_ctr_list))
print('Inconst Neg : ', np.mean(rouge_lcs_inconst_neg_list))
