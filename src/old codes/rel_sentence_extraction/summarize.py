import scores
import sentences      
    
def feature_summ(doc, mode='sents', word_lim=60, sent_lim=3, lam=0.7, mu=0.85):
    '''
    Summarizes the document using features of each sentence as a score
     set mode='words' or mode='sents' according to requirements.
     Also dont forget to choose the limit parameter
    '''

    # Get the feature scores of each sentence
    sent_scores = scores.feature_score(doc)

    # Get the similarity matrix
    sim_matrix = sentences.similarity_matrix(doc, mu=mu)

    # Markov's process
    steady_sent_scores = sentences.markov_process(V=sent_scores, sim=sim_matrix)
    
    # Perform an ILP selection process
    select_sents = sentences.ILP_select(steady_sent_scores, sim_matrix, mode=mode, word_lim=word_lim, sent_lim=sent_lim, lam=lam)

    return select_sents

def LSA_summ(doc, selection='murray', sent_lim=3, mu=0.85, lam=0.7, cross_method=True):
    '''
    Summarises using LSA algorithm. Please set the selection option tou your preferred mode.
    '''
    # decompose the document
    U, S, Vh = sentences.word_SVD(doc)

    if selection == 'gong':
        select_sents = sentences.gong_select(Vh, sent_lim=sent_lim, cross_method=cross_method)

    elif selection == 'stein':
        select_sents = sentences.stein_select(S=S,V=Vh, sent_lim=sent_lim, selection=None, cross_method=cross_method)

    elif selection == 'stein-MMR':
        sim_matrix = sentences.similarity_matrix(doc, mu=mu)
        select_sents = sentences.stein_select(S=S, V=Vh, similarity_matrix=sim_matrix, sent_lim=sent_lim, selection='MMR', lam=lam, cross_method=cross_method)

    elif selection == 'stein-ILP':
        sim_matrix = sentences.similarity_matrix(doc, mu=mu)
        select_sents = sentences.stein_select(S=S, V=Vh, similarity_matrix=sim_matrix, sent_lim=sent_lim, selection='ILP', lam=lam, cross_method=cross_method)

    elif selection == 'murray':
        select_sents = sentences.murray_select(S=S, V=Vh, sent_lim=sent_lim, cross_method=cross_method)
    
    return select_sents