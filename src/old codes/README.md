## Sentence Ranking Model codes
Last updated on December 2019

### Directory structure
1. rel_sentence_extraction : Contain codes to identify the important sentences of a documents that we annotate during ground-truth creation. We only select sentences that has been marked as important by at least one of the multiple text summarization algorithms.
2. Contain codes to compute the different sentence-wise aspects
3. data : a subdirectory contains the associated data files for computing the model comparison table, the sentence mapping from raw text to sequence id and the final scores corresponding to each sentence
4. Pyrouge : Used to compute the ROUGE scores. Taken from the following [Github repository](https://github.com/pcyin/PyRouge)
