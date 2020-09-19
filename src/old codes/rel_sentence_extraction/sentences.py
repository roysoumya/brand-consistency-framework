import nltk
import string
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from ortools.linear_solver import pywraplp

stemmer = nltk.stem.porter.PorterStemmer()
lemmatizer = nltk.stem.WordNetLemmatizer()
remove_punctuation_map = dict((ord(char), ' ') for char in string.punctuation)
integer_chars = [str(digit) for digit in list(range(10))]
remove_integer_map = dict((ord(char), None) for char in integer_chars)

def sentsplit(docs):
    '''
    Splits each document of a document list(collection) into sentences and returns the split list
    '''
    return [nltk.sent_tokenize(doc) for doc in docs]

def stem_tokens(tokens):
    '''
    Transforms a list of words into a list of stemmed words
    '''
    return [stemmer.stem(item) for item in tokens]

def lemm_tokens(tokens):
    '''
    Transforms a list of words into a list of lemmatised words
    '''
    return [lemmatizer.lemmatize(item) for item in tokens]

def filtersent(text, remove_stopwords=True, stem=True, lemm=True, avoid_single_char=True):
    '''
    Filters a sentence according to requirements
    '''
    # remove puctuations and lower the case
    simpletext = text.lower().translate(remove_punctuation_map).translate(remove_integer_map)
    # tokenize
    words = nltk.word_tokenize(simpletext)
    # remove stop words
    if remove_stopwords:
        words = [w for w in words if w not in nltk.corpus.stopwords.words('english')]
    # lemmatize them
    if lemm:
        words = lemm_tokens(words)
    # stem them
    if stem:
        words = stem_tokens(words)
    # avoid single character words
    if avoid_single_char:
        words = [w for w in words if w not in string.ascii_lowercase]
    # detokenise the sentence
    sent = nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(words)
    return sent

def frequency_distrib(essay):
    '''
    Returns a dictionary of words and their counts of occurence in a text(essay)
    '''
    words = nltk.tokenize.word_tokenize(essay)
    return nltk.FreqDist(words)

def similarity_matrix(sentences, mu=0.85):
    '''
    Calculates a similarity matrix between different sentences of an array using a Markovs grid
    '''
    
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(sentences).toarray()
    
    no_sent = len(sentences)
    
    # similarity matrix
    sim = np.zeros((no_sent, no_sent))
    
    for x in range(no_sent):
        for y in range(no_sent):
            adotb = np.dot(count_matrix[x], count_matrix[y])
            a = np.linalg.norm(count_matrix[x])
            b = np.linalg.norm(count_matrix[y])
            if(x==y):
                sim[x,y] = (1-mu)/no_sent
            else:
                sim[x,y] = mu*(adotb/(a*b)) + (1-mu)/no_sent
                
    denom = np.sum(sim,axis=1)
    for x in range(no_sent):
        sim[x,:] = sim[x,:] * 1/denom[x]

    return sim

def markov_process(V, sim):
    '''
    Determines the stable matrix V as a result of Markovs operations on V = sim * V
    '''    
    v = np.array(V)
    while(True):
        v_dash = v.dot(sim)
        if(np.linalg.norm(v_dash - v) < 0.000000001):
            break
        v = v_dash

    return v;

def top_select(v, sent_lim=3):
    '''
    Selects the topmost sentences required
    '''
    n = len(v)
    select_sents = np.zeros(n)
    idx_top_wt = np.argsort(v)
    
    for i in range(sent_lim):
        select_sents[idx_top_wt[n-i-1]] = 1

    return select_sents

def MMR_select(v, redundacy, sent_lim=3, lam=0.7):
    '''
    Select the top sentences by MMR method
    '''
    n = len(v)
    select_sents = np.zeros(n)
    for i in range(sent_lim):
        idx = np.argmax(v)
        select_sents[idx] = 1
        v[idx] = -np.inf
        length_sent = [lam*v[i] - (1-lam)*redundacy[idx,i] for i in range(n)]

    return select_sents

def ILP_select(v,redundacy, mode='sents', word_lim=60, sent_lim=3, lam=0.7):
    '''
    Selects the top dissimilar sentences through an ILP approach. 
    set mode='words' or mode='sents'
    '''

    alpha = {}
    beta = {}
    n = len(v)

    # ILP selection
    solver = pywraplp.Solver('SolveAssignmentProblemMIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # set variables
    for i in range(n):
        alpha[i] = solver.BoolVar('alpha[%i]' % i)

    for i in range(n):
        for j in range(i+1,n):
            beta[i,j] = solver.BoolVar('beta[%i,%i]' %(i,j))

    # objective
    solver.Maximize(solver.Sum(alpha[i]*lam*v[i] for i in range(n)) - solver.Sum([beta[i,j]*(1-lam)*redundacy[i,j] for j in range(i+1,n) for i in range(n)]))

    # constraints
    if mode == 'sents':
        solver.Add( solver.Sum([alpha[i] for i in range(n)]) <= sent_lim)
    elif mode == 'words':
        solver.Add( solver.Sum([alpha[i]*v[i] for i in range(n)]) <= word_lim)

    for i in range(n):
        for j in range(i+1,n):
            solver.Add( beta[i,j] <= alpha[i])
            solver.Add( beta[i,j] <= alpha[j])
            solver.Add( alpha[i] + alpha[j] <= 1 + beta[i,j])

    # solve
    sol = solver.Solve()
    
    alpha_sol = np.int_([alpha[i].solution_value() for i in range(n)])

    return alpha_sol

def word_SVD(doc):
    '''
    Determines a word matrix and performs SVD on it.
    '''
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(doc)
    word_matrix = np.array(X.toarray())

    return np.linalg.svd(word_matrix.T, full_matrices=False)

def gong_select(V, cross_method=True, sent_lim=3):
    '''
    Applies gong liu method to select top sentences from an SVD decomposed matrix
    '''
    n = V.shape[0]

    if cross_method:
        V = V*(V>=np.mean(V,axis=0))

    select_sents = np.zeros(n)
    for i in range(sent_lim):
        sorted_info = np.argsort(V[i,:])
        for j in range(n):
            if select_sents[sorted_info[n-j-1]]==1:
                continue
            else:
                select_sents[sorted_info[n-j-1]]=1
                break

    return np.int_(select_sents)

def stein_select(S, V, similarity_matrix=None, sent_lim=3, cross_method=True, selection='ILP', lam=0.7):
    '''
    Applies Steinberger-Jezek method to select top sentences from an SVD decomposed matrix
    '''
    n = V.shape[0]

    if cross_method:
        V = V*(V>=np.mean(V,axis=0))

    net_weights = S.dot(V)

    if selection == None:
        select_sents = top_select(v=net_weights, sent_lim=sent_lim)

    elif selection == 'MMR':
        select_sents = MMR_select(v=net_weights, redundacy=similarity_matrix, sent_lim=sent_lim, lam=lam)

    elif selection == 'ILP':
        select_sents = ILP_select(v=net_weights, redundacy=similarity_matrix, mode='sents', sent_lim=sent_lim, lam=lam)


    return np.int_(select_sents)

def murray_select(S, V, sent_lim=3, cross_method=True):
    '''
    Applies Murray-et-Al algorithm to 
    '''
    k = sent_lim
    n = V.shape[0]

    if cross_method:
        V = V*(V>=np.mean(V,axis=0))

    # normalised concept weights
    concept_scores = S[:k] * 1/(np.sum(S[:k])) 
    
    select_sents = np.zeros(n)
    selected = 0

    # for each concept
    for i in range(k):
        # until k sentences are seleted
        if(selected>=k):
            break

        X = np.argsort(V[i,:])
        j = 0
        x = 0

        # add sentences until you finish the concept's quota
        while(j<=np.round(concept_scores[i]*k)):
            if(selected>=k):
                break
            if select_sents[X[n-x-1]]==0:
                select_sents[X[n-x-1]] = 1
                j+=1
                selected += 1
            x+=1

    return np.int_(select_sents)