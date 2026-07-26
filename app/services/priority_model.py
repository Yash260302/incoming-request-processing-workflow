import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression

from app.utils.config import Config
from app.utils.logger import Logger


class PriorityModel:
    def __init__(self):
        self.logger = Logger.get_logger()

    def train(self, dataframe):
        self.logger.info("Training Enhanced Priority Champion Model...")
        
        if "subject" in dataframe.columns and "body" in dataframe.columns:
            X = (dataframe["subject"].fillna("") + " " + dataframe["body"].fillna("")).astype(str)
        else:
            X = dataframe["request_text"].astype(str)
        encoder = LabelEncoder()
        y = encoder.fit_transform(dataframe["priority"].astype(str))

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, stratify=y, random_state=42
        )

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english",
            max_features=25000
        )

        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        base_svm = LinearSVC(C=1.5, random_state=42, max_iter=2000)
        calibrated_svm = CalibratedClassifierCV(estimator=base_svm, cv=3)
        lr_model = LogisticRegression(C=3.0, max_iter=1000, random_state=42)

        candidates = [
            ("Calibrated Linear SVM", calibrated_svm),
            ("Tuned Logistic Regression", lr_model)
        ]

        best_model = None
        best_accuracy = 0
        best_name = ""

        for name, model in candidates:
            model.fit(X_train_vec, y_train)
            predictions = model.predict(X_test_vec)
            accuracy = accuracy_score(y_test, predictions)

            self.logger.info(f"{name} Priority Accuracy : {accuracy:.4f}")

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model
                best_name = name

        Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)

        joblib.dump(best_model, Config.MODEL_DIR / "priority_model.pkl")
        joblib.dump(vectorizer, Config.MODEL_DIR / "priority_vectorizer.pkl")
        joblib.dump(encoder, Config.MODEL_DIR / "priority_encoder.pkl")

        self.logger.info("=" * 60)
        self.logger.info(f"Priority Champion Model : {best_name}")
        self.logger.info(f"Accuracy                : {best_accuracy:.4f}")
        self.logger.info("=" * 60)

        return best_model