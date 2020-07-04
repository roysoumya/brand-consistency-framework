# In this program, we say whether a given sentence contains or does not the centrality aspect

import pandas as pd

target_entity_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/OnlyCentralRows_10thSept.csv'
total_aspect_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/SentAspectsFinal1_6thSept.csv'

complete_aspect_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/CompleteSentAspectsFinal_10thSept.csv'

tgt_ent_data = pd.read_csv(target_entity_data_readpath)
tgt_ent_list = list(tgt_ent_data.iloc[:, 1])
sent_data = pd.read_csv(total_aspect_data_readpath)

whetherCentralSent = list()

for row_id in range(sent_data.shape[0]):
    str1 = sent_data.iloc[row_id, 5]
    tgt_list = list()

    if sent_data.iloc[row_id, 6] == 1:
        if str1[0] == '[' and str1[-1] == ']':
            str2 = str1[2:len(str1)-2]
            tgt_list.append(str2)
        else:
            tgt_list.append(sent_data.iloc[row_id, 5])
    elif sent_data.iloc[row_id, 6] > 1:
        str2 = str1[2:len(str1)-2]
        #print(sent_data.iloc[row_id, 5])
        # Converting list string to list
        tgt_list = str2.split("', '")
    print(tgt_list)
    whetherCentral = 0
    if len(tgt_list) == 0:
        whetherCentralSent.append(0)
    else:
        for elem in tgt_list:
            if elem in tgt_ent_list:
                whetherCentral += 1
        whetherCentralSent.append(whetherCentral)

sent_data = sent_data.assign(whetherCentral = whetherCentralSent)
# Check the number of central target entities, the target list contains
sent_data.to_csv(complete_aspect_data_writepath)