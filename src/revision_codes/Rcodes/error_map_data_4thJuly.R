library(dplyr)
error_data = read.csv(file = '../ErrorAnalysisHelperTool3rdJune.csv', header=TRUE)
hybrid_sub = subset(error_data, model_type=='hybrid')
hybrid_sub1 = hybrid_sub %>% select(-model_type)

sent_grp_error_cnt = error_data %>% group_by(row_id, gold_sent) %>% summarise(count = n()) %>% arrange(desc(count))

hybrid_sub2 = merge(hybrid_sub1, sent_grp_error_cnt, by=c('row_id', 'gold_sent'))
hybrid_sub_total_error = merge(hybrid_sub1, error_data, by=c('row_id', 'gold_sent'))

# We now study the points that are misclassified 
hybrid_sub3 = subset(hybrid_sub2, count >= 5 )
write.csv(hybrid_sub3, file = 'SentAllModelFail_4thJuly.csv', row.names = FALSE)

error_map_data = read.csv(file='../ErrorAllModel_SentIdMap4thJune.csv', header=TRUE, stringsAsFactors = FALSE)
error_map_data1 = merge(error_map_data, hybrid_sub3, by='gold_sent')

# Importing sentence aspect information
sent_aspect_scr_data = read.csv(file = 'SubSentDataset_INFO_annotate_13thSept.csv', header = TRUE, stringsAsFactors = FALSE)
sent_aspect_scr_data = sent_aspect_scr_data %>% select(-X.AUTHID)

error_map_data2 = merge(error_map_data1, sent_aspect_scr_data, by='sent_seq_id')
write.csv(error_map_data2, file = 'SentAllModelFail_AspectScores_4thJuly.csv', row.names = FALSE)
