from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from nltk.tokenize import word_tokenize


clean_data_readpath = '/home/soumyadeep/Documents/MSThesisWork/AdobeBrandConsistency/genData1/sentSplitReccoData15thJune.csv'
clean_data = pd.read_csv(clean_data_readpath)

clean_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/negSentsCount_27thAugust.csv'

# Initializing the SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()

authid_list = list()
sent_seq_id_list = list()
sent_content_list = list()
whether_neg_list = list()
neg_scr_list = list()

for row_id in range(clean_data.shape[0]):
    authid_list.append(clean_data.iloc[row_id, 0])
    sent_seq_id_list.append(clean_data.iloc[row_id, 2])

    sent_content = clean_data.iloc[row_id, 1]
    sent_content_list.append(sent_content)
    score1 = vader.polarity_scores(sent_content)
    if len(word_tokenize(sent_content)) >= 5:
        if score1['pos'] < score1['neg']:
            neg_flag=1
        else:
            neg_flag=0
    else:
        neg_flag=0
    whether_neg_list.append(neg_flag)
    neg_scr_list.append(score1['neg'])

    if row_id % 10 == 0:
        print(row_id)

# Only consider sentences having more than 5 words
finalNegSents = pd.DataFrame({'X.AUTHID': authid_list, 'SentSeqId': sent_seq_id_list, 'WhetherNeg': whether_neg_list, 'NegScr': neg_scr_list, 'SentContent': sent_content_list})
finalNegSents.to_csv(clean_data_writepath)