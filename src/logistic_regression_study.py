from parsing_datafile import parse_datafile
import cleaning_text as cleaner 
from vectorizing_text import Vectorizer
from prediction_logistic_regression import LogisticRegression

def simplify_sentiment(sentiments, reduce_sentiments=True):
    """Convertit les string de sentiments en des chiffres
    Args:
        sentiments: liste de sentiments
    Returns:
        Liste de chiffres (minimum à 0) représentant les sentiments
    """
    result = []
    if reduce_sentiments:
        for sent in sentiments:
            low = sent.lower()
            if "positive" in low:
                result.append(2)
            elif "negative" in low:
                result.append(0)
            else:
                result.append(1)
    else:
        sents = ["Extremely Negative", "Negative", "Neutral", "Positive", "Extremely Positive"]
        result = [sents.index(sent) for sent in sentiments]
    return result


if __name__ == "__main__":
    data = parse_datafile('../data/Corona_NLP_train.csv')
    
    big_corpus = cleaner.clean_text('../data/Corona_NLP_train.csv')
    vectorizer = Vectorizer(big_corpus)
    logreg = LogisticRegression(False)
    y_train = simplify_sentiment(data[5], False)

    # Comparaison des résultats avec et sans réduction du nombre de sentiments
    reduced = [True, False]
    for reduce_mode in reduced:
        y_train = simplify_sentiment(data[5], reduce_mode)
        logreg.train(vectorizer.get_score_matrix(), y_train)
        print("Mode nombre de sentiments réduits :", reduce_mode)
        print("Score de précision sur ensemble d'entraînement", logreg.get_score(vectorizer.get_score_matrix(), y_train))