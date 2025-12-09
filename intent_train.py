import csv
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

"""
Scripts that train the Natural Language Processing model.
- Dataset from ./Intent.csv
- Saves weights in models/intent/
    - intent_vectorizer.joblib  (infos about how to transform text -> X)
    - intent_classifier.joblib  (infos about how to transform X -> y)
    
It employs a multinomial logistic regression method with a linear model.
"""
# vectorizer : how to transform text -> X
# clf : how to transform X -> y

def load_dataset_from_csv(csv_path : str | Path) -> tuple[list[str], list[str]]:
    
    # normalize path
    csv_path = Path(csv_path)
    texts : list[str] = []
    labels : list[str] = []
    
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # reads column based on first row of the document
        
        for row in reader:
            text = row["text"]
            label = row["label"]
            texts.append(text)
            labels.append(label)
            
    return texts, labels

def train_intent_model(csv_path : str, model_dir : str = "models/intent"):
    
    texts, labels = load_dataset_from_csv(csv_path)

    
    # splits the data    
    
    X_train_texts, X_test_texts, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,   # 20% data for testing, 80% for training
    stratify=labels, # keeps classes' proportions
    random_state=42  # set the seed for reproducibility
    )
    
    # vectorizes texts as numeric vectors
    # every sentence in the csv is a "document"
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1,1),  # only monogram (each word is a feature). (1,2) bi-grams: "good morning" becomes a feature
        stop_words=None,    # words like articles can be set here in order to be ignored
        max_features=None,  # keeps only the (int)max_features words with most frequency
        min_df=1,           # if integer the word must be in N documents. If float the word must be at least in that fraction of documents
        max_df=1.0,         # if float the word must be in no more than % of the documents. Useful to remove useless repetitve words (like "uuhm")
        #norm="12",          # normalizes each vector TF-IDF to 1 (Euclidean). It prevents longer sentences from having higher weight
        use_idf=True,       # uses IDF (rarity) of words.
        sublinear_tf=True   # prevents repetitions of a word in a single sentence from dominating 
    )
    X_train = vectorizer.fit_transform(X_train_texts)
    X_test = vectorizer.transform(X_test_texts)
    
    #print(X_train)
    
    # actual training
    
    clf = LogisticRegression(max_iter=1000) # if max_iter too small: could not converge
    clf.fit(X_train, y_train)

    # accuracy evaluation
    
    print(f"Results: {clf.predict(X_test)}")
    print(f"Score: {clf.score(X_test, y_test)}")
    
    # saves results
    
    model_dir_path = Path(model_dir)
    model_dir_path.mkdir(
        parents=True,   # creates parents folders if missing
        exist_ok=True   # if dir already exists it does not raise an error
        )
    
    joblib.dump(vectorizer, model_dir_path / "intent_vectorizer.joblib")
    joblib.dump(clf, model_dir_path / "intent_classifier.joblib")

if __name__ == "__main__":
    
    train_intent_model("Intents.csv")