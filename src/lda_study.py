import vectorizing_text as vect
from  lda import LDA
import ldavis

import cleaning_text as cleaner 
if __name__ == "__main__":
    big_corpus = cleaner.clean_text('../data/Corona_NLP_train.csv')
    vectorizer = vect.Vectorizer(big_corpus)
    stop_words = ['the', 'of', 'from', 'a', 'in', 'for', 'to', 'with', 'and']
    words = [word for word in vectorizer.get_dictionary() if word not in stop_words]
    matrix = vectorizer.get_score_matrix()

    n_top_words = 10
    n_iter = 15
    n_topics = 15
    lda = LDA(matrix, n_topics, n_iter)
    c = lda.get()
#    print(c.get_params())
#    print(c.perplexity(matrix))
#    print(c.score(matrix))
#    print(c.components_.shape)
#    print(c.components_)

    for topic_idx, topic in enumerate(lda.get_topics()):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    
    ldavis.do_LDA_visualisation(lda.get_classifier(), matrix, vectorizer.get_vectorizer(), n_topics)
    