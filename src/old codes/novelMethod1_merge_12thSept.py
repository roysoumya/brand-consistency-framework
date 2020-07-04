# Here, we merge the top 3 sentences with the authid

import pandas as pd

#novel_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/NovelMethod1_SentBest3_12thSept.csv'
#novel_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/NovelMethod1_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/BrandConsNegPolarity_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/BrandCons_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/Centrality_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/NegPol_SentBest3_AnnotatePartial_13thSept.csv'
novel_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/Leading_SentBest3_AnnotatePartial_13thSept.csv'

novel_data = pd.read_csv(novel_data_readpath)

#novel_data2_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/NovelMethod1_sidebyside_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data2_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/BrandConsNegPolarity_sidebyside_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data2_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/BrandCons_sidebyside_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data2_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/Centrality_sidebyside_SentBest3_AnnotatePartial_13thSept.csv'
#novel_data2_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/NegPol_sidebyside_SentBest3_AnnotatePartial_13thSept.csv'
novel_data2_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/Leading_sidebyside_SentBest3_AnnotatePartial_13thSept.csv'

# sentence data is at column no. 13 (indexed at 0)
top1_list = list()
top2_list = list()
top3_list = list()
authid_list = list()

for row_id in range(novel_data.shape[0]):
    if novel_data.iloc[row_id, 14] == 1:
        authid_list.append(novel_data.iloc[row_id, 0])
        top1_list.append(novel_data.iloc[row_id, 13])
    elif novel_data.iloc[row_id, 14] == 2:
        top2_list.append(novel_data.iloc[row_id, 13])
    elif novel_data.iloc[row_id, 14] == 3:
        top3_list.append(novel_data.iloc[row_id, 13])

#novel_df = pd.DataFrame({'X.AUTHID': authid_list, 'Hybrid1': top1_list, 'Hybrid2': top2_list, 'Hybrid3': top3_list})
#novel_df = pd.DataFrame({'X.AUTHID': authid_list, 'Hybrid1': top1_list, 'Hybrid2': top2_list, 'Hybrid3': top3_list})
#novel_df = pd.DataFrame({'X.AUTHID': authid_list, 'InconsNeg1': top1_list, 'InconsNeg2': top2_list, 'InconsNeg3': top3_list})
#novel_df = pd.DataFrame({'X.AUTHID': authid_list, 'Incons1': top1_list, 'Incons2': top2_list, 'Incons3': top3_list})
#novel_df = pd.DataFrame({'X.AUTHID': authid_list, 'Ctr1': top1_list, 'Ctr2': top2_list, 'Ctr3': top3_list})
#novel_df = pd.DataFrame({'X.AUTHID': authid_list, 'Neg1': top1_list, 'Neg2': top2_list, 'Neg3': top3_list})
novel_df = pd.DataFrame({'X.AUTHID': authid_list, 'LeadN1': top1_list, 'LeadN2': top2_list, 'LeadN3': top3_list})
novel_df.to_csv(novel_data2_writepath)