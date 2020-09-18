library(dplyr)

cont_tab_data = read.csv(file='../McnemarContTable_7thJuly.csv', header=TRUE)

stats1 = '
> sum(cont_tab_data$HYBRID)
[1] 48
> sum(cont_tab_data$CTR)
[1] 45
> sum(cont_tab_data$INCONS_NEG)
[1] 38
> sum(cont_tab_data$INCONS)
[1] 37
> sum(cont_tab_data$NEG)
[1] 37
> sum(cont_tab_data$LEAD)
[1] 25
> sum(cont_tab_data$RAND)
[1] 0
'

# performing paired t-test
t.test(cont_tab_data$CTR, cont_tab_data$HYBRID, paired = TRUE)
t.test(cont_tab_data$INCONS, cont_tab_data$HYBRID, paired = TRUE)

ttest_result = '
> t.test(cont_tab_data$CTR, cont_tab_data$HYBRID, paired = TRUE)

	Paired t-test

data:  cont_tab_data$CTR and cont_tab_data$HYBRID
t = -0.9037, df = 98, p-value = 0.3684
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -0.09684683  0.03624077
sample estimates:
mean of the differences 
            -0.03030303 

> t.test(cont_tab_data$INCONS_NEG, cont_tab_data$HYBRID, paired = TRUE)

	Paired t-test

data:  cont_tab_data$INCONS_NEG and cont_tab_data$HYBRID
t = -1.9151, df = 98, p-value = 0.05839
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -0.205678113  0.003657911
sample estimates:
mean of the differences 
             -0.1010101 
             
> t.test(cont_tab_data$INCONS, cont_tab_data$HYBRID, paired = TRUE)

	Paired t-test

data:  cont_tab_data$INCONS and cont_tab_data$HYBRID
t = -2.1556, df = 98, p-value = 0.03356
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -0.213401795 -0.008820427
sample estimates:
mean of the differences 
             -0.1111111 
'
cor.test(cont_tab_data$CTR, cont_tab_data$HYBRID)

cont_hyb_ctr = subset(cont_tab_data, HYBRID == 1 | CTR == 1)
cont_hyb_incons = subset(cont_tab_data, HYBRID == 1 | INCONS == 1)
cont_hyb_incons_neg = subset(cont_tab_data, HYBRID == 1 | INCONS_NEG == 1)

t.test(cont_hyb_ctr$CTR, cont_hyb_ctr$HYBRID, paired = TRUE)
chisq.test(cont_hyb_ctr$CTR, cont_hyb_ctr$HYBRID, correct = FALSE)

t.test(cont_hyb_incons$INCONS, cont_hyb_incons$HYBRID, paired = TRUE)
t.test(cont_hyb_incons_neg$INCONS_NEG, cont_hyb_incons_neg$HYBRID, paired = TRUE)

stats3 = '
> t.test(cont_hyb_ctr$CTR, cont_hyb_ctr$HYBRID, paired = TRUE)

	Paired t-test

data:  cont_hyb_ctr$CTR and cont_hyb_ctr$HYBRID
t = -0.90293, df = 51, p-value = 0.3708
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -0.18596655  0.07058193
sample estimates:
mean of the differences 
            -0.05769231 

> t.test(cont_hyb_incons$INCONS, cont_hyb_incons$HYBRID, paired = TRUE)

	Paired t-test

data:  cont_hyb_incons$INCONS and cont_hyb_incons$HYBRID
t = -2.1873, df = 55, p-value = 0.03299
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -0.37639919 -0.01645795
sample estimates:
mean of the differences 
             -0.1964286 

> t.test(cont_hyb_incons_neg$INCONS_NEG, cont_hyb_incons_neg$HYBRID, paired = TRUE)

	Paired t-test

data:  cont_hyb_incons_neg$INCONS_NEG and cont_hyb_incons_neg$HYBRID
t = -1.9348, df = 56, p-value = 0.05808
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -0.357086365  0.006209172
sample estimates:
mean of the differences 
             -0.1754386 

'

curr_data = read.csv(file = '../All_model_significance_10thJuly.csv', header=TRUE, stringsAsFactors=FALSE)
curr_hyb_ctr = subset(curr_data, HYBRID == 1 | CTR == 1)

table(cont_hyb_ctr$CTR, cont_hyb_ctr$HYBRID)

chisq.test(curr_data$CTR, curr_data$HYBRID, correct = FALSE)
fisher.test(curr_data$CTR, curr_data$HYBRID)

chisq.test(curr_hyb_ctr$CTR, curr_hyb_ctr$HYBRID, correct = FALSE)
fisher.test(curr_hyb_ctr$CTR, curr_hyb_ctr$HYBRID)

result1 = '
> chisq.test(curr_hyb_ctr$CTR, curr_hyb_ctr$HYBRID, correct = FALSE)

	Pearsons Chi-squared test

data:  curr_hyb_ctr$CTR and curr_hyb_ctr$HYBRID
X-squared = 5.8244, df = 1, p-value = 0.01581
'

cont_hyb_incons = subset(cont_tab_data, HYBRID == 1 | INCONS == 1)
cont_hyb_incons_neg = subset(cont_tab_data, HYBRID == 1 | INCONS_NEG == 1)

t.test(cont_hyb_ctr$CTR, cont_hyb_ctr$HYBRID)
t.test(cont_hyb_incons$INCONS, cont_hyb_incons$HYBRID, paired = TRUE)
t.test(cont_hyb_incons_neg$INCONS_NEG, cont_hyb_incons_neg$HYBRID, paired = TRUE)

library(DescTools)
GTest(curr_hyb_ctr$CTR, curr_hyb_ctr$HYBRID)
result5 = '
> GTest(curr_hyb_ctr$CTR, curr_hyb_ctr$HYBRID)

	Log likelihood ratio (G-test) test of independence without correction

data:  curr_hyb_ctr$CTR and curr_hyb_ctr$HYBRID
G = 9.6416, X-squared df = 1, p-value = 0.001902
'

check_data = read.csv(file = '../CheckData_11thJuly.csv', header = TRUE, stringsAsFactors = FALSE)
aspect_data = read.csv(file = 'SubSentDataset_INFO_annotate_13thSept.csv', header = TRUE, stringsAsFactors = FALSE)

seq_id_data = read.csv(file = 'FinalMappedAnnotatedINFOsents_17thSept.csv', header = TRUE, stringsAsFactors = FALSE)

aspect_data1 = merge(aspect_data, seq_id_data, by=c('X.AUTHID', 'sent_seq_id'))
aspect_data2 = subset(aspect_data1, sent_rec_scr > 3)

write.csv(aspect_data2, file = 'MASR_AllRelevant_Above3_11thJuly.csv', row.names = FALSE)




aspect_data_rel = subset(aspect_data, sent_rec_scr > 3)
gold_data1 = read.csv(file = '../GoldDataSentenceMap_11thJuly.csv', header = TRUE, stringsAsFactors = FALSE)

gold_ids = gold_data1$sent_seq_id
`%notin%` = Negate(`%in%`)

aspect_data_rel1 = subset(aspect_data, sent_seq_id %notin% gold_ids)

aspect_sub = merge(aspect_data, check_data, by='X.AUTHID', sort=FALSE)
aspect_sub1 = aspect_sub %>% arrange(X.AUTHID, desc(sent_rec_scr))
        
        subset(aspect_data, X.AUTHID %in% check_data$X.AUTHID)
aspect_sub = aspect_sub %>% arrange(desc(sent_rec_scr), sent_seq_id)
