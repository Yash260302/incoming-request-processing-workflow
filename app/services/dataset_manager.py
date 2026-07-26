from pathlib import Path

import pandas as pd

from app.utils.config import Config
from app.utils.logger import Logger


class DatasetManager:

    def __init__(self):

        self.logger = Logger.get_logger()

        self.dataset = None

    # ---------------------------------------------------------

    def load_dataset(self):

        self.logger.info("Loading processed dataset...")

        self.dataset = pd.read_csv(
            Config.PROCESSED_DATASET
        )

        self.logger.info(
            f"Loaded {len(self.dataset)} records."
        )

        return self.dataset

    # ---------------------------------------------------------

    def validate_dataset(self):

        required_columns = [

            "request_text",

            "queue",

            "priority",

            "type",

            "language",

            "answer"

        ]

        missing = [

            column

            for column in required_columns

            if column not in self.dataset.columns

        ]

        if missing:

            raise Exception(

                f"Missing columns: {missing}"

            )

        self.logger.info(

            "Dataset validation successful."

        )

    # ---------------------------------------------------------

    def english_only(self):

        english = self.dataset[

            self.dataset["language"]

            == "en"

        ]

        self.logger.info(

            f"English Records : {len(english)}"

        )

        return english

    # ---------------------------------------------------------

    def sample(self, size=5):

        return self.dataset.sample(size)

    # ---------------------------------------------------------

    def statistics(self):

        self.logger.info("Dataset Statistics")

        self.logger.info(

            f"Rows : {len(self.dataset)}"

        )

        self.logger.info(

            f"Columns : {len(self.dataset.columns)}"

        )

        self.logger.info(

            f"Queues : {self.dataset['queue'].nunique()}"

        )

        self.logger.info(

            f"Priority Levels : {self.dataset['priority'].nunique()}"

        )

        self.logger.info(

            f"Types : {self.dataset['type'].nunique()}"

        )