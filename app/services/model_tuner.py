from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier


class ModelTuner:

    @staticmethod
    def random_forest():

        model = RandomForestClassifier(
            random_state=42,
            n_jobs=-1
        )

        parameters = {

            "n_estimators": [200, 300, 500],

            "max_depth": [
                None,
                20,
                40,
                60
            ],

            "min_samples_split": [
                2,
                5,
                10
            ],

            "min_samples_leaf": [
                1,
                2,
                4
            ]
        }

        return model, parameters

    @staticmethod
    def linear_svm():

        model = LinearSVC(
            random_state=42
        )

        parameters = {

            "C": [
                0.1,
                1,
                10,
                100
            ]
        }

        return model, parameters

    @staticmethod
    def xgboost():

        model = XGBClassifier(
            eval_metric="mlogloss",
            tree_method="hist",
            random_state=42
        )

        parameters = {

            "n_estimators": [
                200,
                400
            ],

            "max_depth": [
                6,
                8,
                10
            ],

            "learning_rate": [
                0.01,
                0.05,
                0.1
            ],

            "subsample": [
                0.8,
                1.0
            ]
        }

        return model, parameters