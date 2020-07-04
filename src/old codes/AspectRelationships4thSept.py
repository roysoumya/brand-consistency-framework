# Here, we study the relationship among the sentence ranking aspects
import pandas as pd

# Reading the relevant files
sent_aspect_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/sentFinalRankingWithCentrality1stSeptember.csv'
sent_seq_id_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/sentSplitReccoData15thJune.csv'

sent_aspect_data = pd.read_csv(sent_aspect_data_readpath)
# This file contains the mapped sentences to sequence ids
sent_seq_id_data = pd.read_csv(sent_seq_id_data_readpath)

