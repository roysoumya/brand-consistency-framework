# This is the final program that computes the target entities for a given sentence

import pandas as pd
import spacy
import neuralcoref
import nltk
from collections import defaultdict


# In this program, we taken a sentence and a target word as input and return the complete name of the entity it is a part of.
def postagEntity(sentence, target):
    pos_tag_sent = nltk.pos_tag(nltk.word_tokenize(sentence))
    entity_name = ""
    index = 0
    for word, pos_tag in pos_tag_sent:
        if word == target:
            # We now check the postag associated with the target word
            entity_name = ""
            if pos_tag == 'NN' or pos_tag=='NNS' or pos_tag=='NNP':
                entity_name = word
                # Now in order to get the complete entity name. We check the previous words and continue appending them in front of them
                for elem_id in range(index-1, -1, -1):
                    word1, pos_tag1 = pos_tag_sent[elem_id]
                    if pos_tag1 == 'NN' or pos_tag1 == 'NNS' or pos_tag1 == 'NNP':
                        entity_name = word1 + ' ' + entity_name
                    else:
                        return entity_name
            elif pos_tag == 'PRP' or pos_tag == 'PRP$':
                entity_name = word
                # Now in order to get the complete entity name. We check the previous words and continue appending them in front of them
                for elem_id in range(index - 1, -1, -1):
                    word1, pos_tag1 = pos_tag_sent[elem_id]
                    if pos_tag1 == 'PRP' or pos_tag1 == 'PRP$':
                        entity_name = word1 + ' ' + entity_name
                    else:
                        # We also check in the coref-clusters whether the pronoun is referred to an entity
                        return entity_name
            else:
                break
        index += 1

    return entity_name


nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)


# Spacy coref is working. Now test on our 202 articles. And try to identify the target entities and at the end, check the target entity of a given sentence
# We start by taking a window of 3 sentences each.
clean_data_readpath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/recoFinalcleanData19thAugust.csv'
clean_data = pd.read_csv(clean_data_readpath)

target_entity_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/sentLevelTargetEntities_31stAugust.csv'
mismatch_data_writepath = '/home/soumyadeep/PycharmProjects/MSThesisWorkMay2019/JournalCodes/data/mismatchData31stAugust.csv'
# The aim of this part of the code is to identify the target entity of a given sentence. Usually we consider the 'subj' to be the target entity
# If that target entity turns out to be a pronoun, we use reference resolution to resolve the issue. Also if there are multiple target entities.
no_subj_auth_ids = list()

# We now save the file containing the target entities for a given sentence

authid_list = list()
sent_seq_id_list = list()
sentence_list = list()
target_entities_list = list()
target_ent_size_list = list()

sents_new_list = list()
sents_old_list = list()

for row_id in range(clean_data.shape[0]):
    nlp_para = nlp(clean_data.iloc[row_id, 2])
    new_para = nlp_para._.coref_resolved
    new_para1 = new_para
    #sentences = sent_tokenize(clean_data.iloc[row_id, 2])
    sentences = nltk.sent_tokenize(new_para1)
    num_of_sents = len(sentences)

    sentences_old = nltk.sent_tokenize(clean_data.iloc[row_id, 2])

    if len(sentences_old) == num_of_sents:
        print(row_id, len(sentences_old), num_of_sents)
        authid_list.append(clean_data.iloc[row_id, 0])
        sents_old_list.append(sentences_old)
        sents_new_list.append(sentences)
    else:


#mismatch_data = pd.DataFrame({'X.AUTHID': authid_list, 'sents_old': sents_old_list, 'sents_new': sents_new_list})
#mismatch_data.to_csv(mismatch_data_writepath, sep='|')

'''

    if row_id % 10 == 0:
        print(row_id)

    for sent_id in range(num_of_sents):
        authid_list.append(clean_data.iloc[row_id, 0])
        sent_seq_id_list.append(sent_id)
        sentence_list.append(sentences[sent_id])


        nlp_sent = nlp(sentences[sent_id])
        sub_toks = [tok for tok in nlp_sent if (tok.dep_ == 'nsubj')]

        # When there is no 'nsubj' in the sentence, we store their authids
        if len(sub_toks) == 0:
            no_subj_auth_ids.append(clean_data.iloc[row_id, 0])
            target_entities_list.append('(No subject)')
            target_ent_size_list.append(0)
            #print(sentences[sent_id], sub_toks, ' (No subject) ', nlp_sent._.coref_clusters)
        elif len(sub_toks) == 1:
            # This means there is no nsubj ambiguation
            entity_name = postagEntity(sentences[sent_id], sub_toks[0].text)
            target_entities_list.append(entity_name)
            target_ent_size_list.append(1)
            #print(sentences[sent_id], sub_toks, entity_name, nlp_sent._.coref_clusters)
        else:
            # Currently facing problem with sentences having multiple 'nsubj's
            entity_name_list = list()
            for sub_toks_each in sub_toks:
                entity_name = postagEntity(sentences[sent_id], sub_toks_each.text)
                if entity_name != "":
                    entity_name_list.append(entity_name)
            target_entities_list.append(entity_name_list)
            target_ent_size_list.append(len(entity_name_list))
            #print(sentences[sent_id], sub_toks, entity_name_list, nlp_sent._.coref_clusters)
   

target_entity_data = pd.DataFrame({'X.AUTHID': authid_list, 'sent_seq_id': sent_seq_id_list, 'sent_content': sentence_list,
                                   'target_entities': target_entities_list, 'target_ent_size': target_ent_size_list})
target_entity_data.to_csv(target_entity_data_writepath, sep='|')

'''