import nltk
import sentences
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import wordnet
import numpy as np

def position_score(pos):
    '''
    Returns a score based on position of the word in the sentence
    '''
    if(pos<=0.1):
        return 0.17
    elif(pos<=0.2):
        return 0.23
    elif(pos<=0.3):
        return 0.14
    elif(pos<=0.4):
        return 0.08
    elif(pos<=0.5):
        return 0.05
    elif(pos<=0.6):
        return 0.04
    elif(pos<=0.7):
        return 0.06
    elif(pos<=0.8):
        return 0.04
    elif(pos<=0.9):
        return 0.04
    else:
        return 0.15
    
def POS_score(word):
    '''
    Returns a score based on the part of speech tag of the word
    '''
    pos_tag = nltk.pos_tag([word])[0][1]
    return 1

def fam_func(fam):
    '''
    A function to calculate familiarity score
    '''
    # limit tends to 1 for fam=0
    if(fam==0):
        return 1
    # the formula
    return 1/(1+np.exp( -8 * (-0.5 + 1/fam) ))

def familiarity_score(word):
    '''
    Returns the familiarity score of a word. Uses number of synonyms as a familiarity metric
    '''
    synonyms = 0
    for syn in wordnet.synsets("active"):
        synonyms += len(syn.lemmas())        
    return fam_func(synonyms)

def feature_score(doc):
    '''
    scores sentences based on certain features and returns a matrix of their scores
    '''
    no_sent = len(doc)
    
    # the frequency distribution of each word in the document
    essay = TreebankWordDetokenizer().detokenize([string for string in doc])
    freq_dist = sentences.frequency_distrib(essay)
    
    # tf word
    tf_word = {word: freq for word, freq in freq_dist.items() if not word.isdigit()}
    
    # length of word
    len_word = {word: len(word) for word in freq_dist.keys()}
    
    # pos tag
    pos_word = {word: POS_score(word) for word in freq_dist.keys()}
    
    # familiarity
    fam_word = {word: familiarity_score(word) for word in freq_dist.keys()}
    
    score_sents = []
    for i in range(no_sent):
        score_sent = 0
        
        for j,word in enumerate(nltk.tokenize.word_tokenize(doc[i])):
            # occurence score
            occ_word = position_score( j/len(doc[i]) )
            
            score_word = tf_word[word] * len_word[word] * pos_word[word] * fam_word[word] * occ_word
            score_sent += score_word
            
            
            # corefferant
            if(pos_word[word]=='PRP'):
                if(j/len(corpus[s][i]) < 0.5):
                    if(i>0):
                        score_sent += score_sents[i-1]/len(nltk.tokenize.word_tokenize(doc[i-1]))
                else:
                    score_sent += score_sent/len(nltk.tokenize.word_tokenize(doc[i]))
        
        score_sents.append(score_sent)
    
    return score_sents