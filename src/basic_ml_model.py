import pandas as pd
from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from pprint import pprint
from time import time
from sklearn.metrics import accuracy_score, classification_report


def load_data(file: str) -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=file)


def split_X_y(train_df: pd.DataFrame, test_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    y_train = train_df["target"]
    X_train = train_df[["id", "text"]]

    X_test = test_df
    return X_train, y_train, X_test


def grid_search(X_train: pd.DataFrame, y_train: pd.Series):
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("clf", SGDClassifier()),
        ]
    )

    params = {
        "tfidf__ngram_range": ((1, 1), (1, 2)),
        "clf__alpha": (0.001, 0.0001, 0.00001, 0.000001),
        "clf__penalty": ("l2", "elasticnet"),
        "clf__max_iter": (20, 50, 100, 1000),
    }

    grid_search = GridSearchCV(pipeline, param_grid=params, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(params)
    t0 = time()
    grid_search.fit(X_train["text"], y_train)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(params.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    return


def train(X_train: pd.DataFrame, y_train: pd.Series) -> Tuple[TfidfVectorizer, SGDClassifier]:
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_vectorized = vectorizer.fit_transform(X_train["text"])

    model = SGDClassifier(alpha=0.0001, max_iter=100, penalty="elasticnet")
    model.fit(X_vectorized, y_train)

    y_pred = model.predict(X_vectorized)

    print("Accuracy score = ", accuracy_score(y_true=y_train, y_pred=y_pred))
    print("Classification report:-")
    print(classification_report(y_true=y_train, y_pred=y_pred))

    return vectorizer, model


def predict(X_test: pd.DataFrame, vect: TfidfVectorizer, model: SGDClassifier) -> pd.DataFrame:
    X_test_vectorized = vect.transform(X_test["text"])
    y_pred = model.predict(X_test_vectorized)

    print(X_test_vectorized.shape, y_pred.shape)

    y_final = pd.concat(
        [X_test["id"], pd.Series(y_pred, index=X_test.index, name="target")], axis=1
    )
    print(y_final.shape)
    print(y_final.columns)

    return y_final


if __name__ == "__main__":
    train_df = load_data(file="data/cleaned_train.csv")
    test_df = load_data(file="data/cleaned_test.csv")

    X_train, y_train, X_test = split_X_y(train_df=train_df, test_df=test_df)

    # grid_search(X_train=X_train, y_train=y_train)

    vectorizer, model = train(X_train=X_train, y_train=y_train)

    # Testing
    y_test = predict(X_test=X_test, vect=vectorizer, model=model)

    print(y_test.head())

    y_test.to_csv("output/basic_submission.csv", index=False)
