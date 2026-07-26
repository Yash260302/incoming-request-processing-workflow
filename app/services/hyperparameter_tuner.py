import joblib

from sklearn.model_selection import RandomizedSearchCV

from app.utils.config import Config
from app.utils.logger import Logger


class HyperparameterTuner:

    def __init__(self):

        self.logger = Logger.get_logger()

    def tune(
        self,
        name,
        model,
        parameters,
        X_train,
        y_train
    ):

        self.logger.info(f"Tuning {name}...")

        search = RandomizedSearchCV(
            estimator=model,
            param_distributions=parameters,
            n_iter=5,
            scoring="accuracy",
            cv=3,
            verbose=2,
            random_state=42,
            n_jobs=-1
        )

        search.fit(X_train, y_train)

        self.logger.info(
            f"Best Accuracy ({name}): {search.best_score_:.4f}"
        )

        self.logger.info(
            f"Best Parameters: {search.best_params_}"
        )

        model_path = (
            Config.MODEL_DIR /
            f"{name.lower().replace(' ', '_')}_best.pkl"
        )

        joblib.dump(
            search.best_estimator_,
            model_path
        )

        return search.best_estimator_