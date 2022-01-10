import cst 
from sklearn.neighbors import KNeighborsClassifier
import cleaning_text as cleaner 
from vectorizing_text import Vectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def KNeighbors():
    X = cleaner.clean_text(cst.TRAIN)
    print (X)
    y = cleaner.read_column(cst.TRAIN, 5)
    vectorizer = Vectorizer(X)
    matrix = vectorizer.get_score_matrix()
    X_train, X_test, y_train, y_test = train_test_split(matrix, y, test_size = 0.30)
    k=1
    for k  in range(1,30,5):
        model = KNeighborsClassifier(n_neighbors = k)
        model.fit(X_train,y_train)
        predictions = model.predict(X_test)
        scores = (accuracy_score(y_test,predictions))
        print(scores)

if __name__ == "__main__":
     KNeighbors()




