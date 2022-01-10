from sklearn.decomposition import LatentDirichletAllocation

class LDA:
    def __init__(self, vect_corpus, n_components, max_iter):
        self.classifier = LatentDirichletAllocation(n_components, max_iter=max_iter,n_jobs=-1)
        self.classifier.fit(vect_corpus)
    
    def get(self):
        return self.classifier
    
    def get_topics(self):
        return self.classifier.components_
    
    def get_classifier(self):
        return self.classifier
