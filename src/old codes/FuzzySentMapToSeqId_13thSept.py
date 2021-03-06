# Here, we map the sentences that have changed after performing reference resolution. We obtain a fuzzy similarity metric
# that calculates the edit distance similarity value and performs a thresholding value. We obtain a

import pandas as pd
from collections import defaultdict
import nltk


def levenSimScr(sent1, sent2):
    edit_dist = nltk.edit_distance(sent1, sent2)
    #print(sent1, sent2)
    edit_sim = 1.0 - edit_dist/max(len(nltk.word_tokenize(sent1)), len(nltk.word_tokenize(sent2)))
    return edit_sim


# Reading the python data files
sent_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/sentSplitReccoData15thJune.csv'
target_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/AnnotatedINFOsents_13thSept.csv'
sent_data = pd.read_csv(sent_data_readpath)
target_data = pd.read_csv(target_data_readpath)

target_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/MappedAnnotatedINFOsents_13thSept.csv'

# Re-check this part with proper substitution


# We first create a dictionary for a x_authid with the sequence ids.
# key - Authid, value: List of sequence ids
sent_data_sent_dict = defaultdict(list)
sent_data_seq_id_dict = defaultdict(list)
annot_data_sent_dict = defaultdict(list)
#new_data_seq_id_dict = defaultdict(list)

for row_id in range(sent_data.shape[0]):
    sent_data_sent_dict[sent_data.iloc[row_id, 0]].append(sent_data.iloc[row_id, 1])
    sent_data_seq_id_dict[sent_data.iloc[row_id, 0]].append(sent_data.iloc[row_id, 2])

for row_id1 in range(target_data.shape[0]):
    annot_data_sent_dict[target_data.iloc[row_id1, 0]].append(target_data.iloc[row_id1, 1])
    #new_data_seq_id_dict[new_data.iloc[row_id1, 0]].append(new_data.iloc[row_id1, 1])

# We now check within the same web page, having the same X.AUTHID, whether the sentences are highly similar
# Having a levenshtein score similarity of more than 0.8 Fuzzy similarity

print('Dictionary preparation is done.')

sent_sents_list = list()
sent_sent_seq_id_list = list()
annot_sents_list = list()
#new_sent_seq_id_list = list()
edit_sim_scr_list = list()
authid_list = list()
comp_inc = 0

for key_one in annot_data_sent_dict.keys():
    annot_data_sents = annot_data_sent_dict[key_one]
    #new_data_seqids = new_data_seq_id_dict[key_one]
    sent_data_sents = sent_data_sent_dict[key_one]
    sent_data_seqids = sent_data_seq_id_dict[key_one]

    # For such authids sentences do exist
    if len(annot_data_sents) > 0 and len(sent_data_sents) > 0:
        # We will print the pair of sentences that a levenshtein similarity score of >= 0.85
        for sent_row_id in range(len(sent_data_sents)):
            for annot_row_id in range(len(annot_data_sents)):
                #print(sent_row_id, annot_row_id)
                #print(sent_data_sents[sent_row_id], annot_data_sents[annot_row_id])
                sim_scr = levenSimScr(sent_data_sents[sent_row_id], annot_data_sents[annot_row_id])
                if sim_scr >= 0.5:
                    #print(old_data_sents[old_row_id], new_data_sents[new_row_id])
                    sent_sents_list.append(sent_data_sents[sent_row_id])
                    sent_sent_seq_id_list.append(sent_data_seqids[sent_row_id])
                    annot_sents_list.append(annot_data_sents[annot_row_id])
                    #new_sent_seq_id_list.append(new_data_seqids[new_row_id])
                    edit_sim_scr_list.append(sim_scr)
                    authid_list.append(key_one)

    if comp_inc % 10 == 0:
        print(comp_inc)
        outputDf = pd.DataFrame(
            {'X.AUTHID': authid_list, 'sent_sent_seq_id': sent_sent_seq_id_list, 'sent sent': sent_sents_list,
             'annot sent': annot_sents_list, 'sim scr': edit_sim_scr_list})
        outputDf.to_csv(target_data_writepath)
    comp_inc += 1


outputDf = pd.DataFrame({'X.AUTHID': authid_list, 'sent_sent_seq_id': sent_sent_seq_id_list, 'sent sent': sent_sents_list,
                         'annot sent': annot_sents_list, 'sim scr': edit_sim_scr_list})
outputDf.to_csv(target_data_writepath)