# Here, we map the sentences that have changed after performing reference resolution. We obtain a fuzzy similarity metric
# that calculates the edit distance similarity value and performs a thresholding value. We obtain a

import pandas as pd
from collections import defaultdict
import nltk


def levenSimScr(sent1, sent2):
    edit_dist = nltk.edit_distance(sent1, sent2)
    edit_sim = 1.0 - edit_dist/max(len(nltk.word_tokenize(sent1)), len(nltk.word_tokenize(sent2)))
    return edit_sim


# Reading the python data files
old_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/oldData1_31stAugust.csv'
new_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/newData1_31stAugust.csv'
old_data = pd.read_csv(old_data_readpath)
new_data = pd.read_csv(new_data_readpath)

target_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/targetDataTest31stAugust.csv'

# We first create a dictionary for a x_authid with the sequence ids.
# key - Authid, value: List of sequence ids
old_data_sent_dict = defaultdict(list)
old_data_seq_id_dict = defaultdict(list)
new_data_sent_dict = defaultdict(list)
new_data_seq_id_dict = defaultdict(list)

for row_id in range(old_data.shape[0]):
    old_data_sent_dict[old_data.iloc[row_id, 0]].append(old_data.iloc[row_id, 2])
    old_data_seq_id_dict[old_data.iloc[row_id, 0]].append(old_data.iloc[row_id, 1])

for row_id1 in range(new_data.shape[0]):
    new_data_sent_dict[new_data.iloc[row_id1, 0]].append(new_data.iloc[row_id1, 2])
    new_data_seq_id_dict[new_data.iloc[row_id1, 0]].append(new_data.iloc[row_id1, 1])

# We now check within the same web page, having the same X.AUTHID, whether the sentences are highly similar
# Having a levenshtein score similarity of more than 0.8 Fuzzy similarity

print('Dictionary preparation is done.')

old_sents_list = list()
old_sent_seq_id_list = list()
new_sents_list = list()
new_sent_seq_id_list = list()
edit_sim_scr_list = list()
authid_list = list()
comp_inc = 0

for key_one in new_data_sent_dict.keys():
    new_data_sents = new_data_sent_dict[key_one]
    new_data_seqids = new_data_seq_id_dict[key_one]
    old_data_sents = old_data_sent_dict[key_one]
    old_data_seqids = old_data_seq_id_dict[key_one]

    # For such authids sentences do exist
    if len(new_data_sents) > 0 and len(old_data_sents) > 0:
        # We will print the pair of sentences that a levenshtein similarity score of >= 0.85
        for old_row_id in range(len(old_data_sents)):
            for new_row_id in range(len(new_data_sents)):
                sim_scr = levenSimScr(old_data_sents[old_row_id], new_data_sents[new_row_id])
                if sim_scr >= 0.5:
                    #print(old_data_sents[old_row_id], new_data_sents[new_row_id])
                    old_sents_list.append(old_data_sents[old_row_id])
                    old_sent_seq_id_list.append(old_data_seqids[old_row_id])
                    new_sents_list.append(new_data_sents[new_row_id])
                    new_sent_seq_id_list.append(new_data_seqids[new_row_id])
                    edit_sim_scr_list.append(sim_scr)
                    authid_list.append(key_one)

    if comp_inc % 10 == 0:
        print(comp_inc)
    comp_inc += 1


outputDf = pd.DataFrame({'X.AUTHID': authid_list, 'old_sent_seq_id': old_sent_seq_id_list, 'old sent': old_sents_list,
                         'new_sent_seq_id': new_sent_seq_id_list, 'new sent': new_sents_list, 'sim scr': edit_sim_scr_list})
outputDf.to_csv(target_data_writepath)