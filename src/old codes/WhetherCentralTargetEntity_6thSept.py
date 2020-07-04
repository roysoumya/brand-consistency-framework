# In this program, we take as input -- SentAspectsFinal1_6thSept.csv file as input and develop a rule-based method
# for classifying whether at least one of the target entities belong to the 'WhetherCentral' class

import pandas as pd

sent_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/SentAspectsFinal1_6thSept.csv'
sent_data = pd.read_csv(sent_data_readpath)

target_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/CentralityTargetAspects_9thSept.csv'


# Columns - 5 and 6 (indexed from 0)
list1 = list()
for row_id in range(sent_data.shape[0]):
    str1 = sent_data.iloc[row_id, 5]
    if sent_data.iloc[row_id, 6] == 1:
        if str1[0] == '[' and str1[-1] == ']':
            str2 = str1[2:len(str1)-2]
            list1.append(str2)
        else:
            list1.append(sent_data.iloc[row_id, 5])
    elif sent_data.iloc[row_id, 6] > 1:
        str2 = str1[2:len(str1)-2]
        #print(sent_data.iloc[row_id, 5])
        # Converting list string to list
        list1.extend(str2.split("', '"))

from collections import Counter
word_counter = Counter(list1)
print(word_counter.most_common(100))

keys_list = list(set(list1))
values_list = list()
for elem in keys_list:
    values_list.append(word_counter[elem])


data_pd = pd.DataFrame({'target_entity': keys_list, 'count': values_list})
data_pd.to_csv(target_data_writepath)
