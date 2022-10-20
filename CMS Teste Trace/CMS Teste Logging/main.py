import logging

# instantiate logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# define handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)  # add formatter to handler
logger.addHandler(handler)  # add handler to logger


if __name__ == "__main__":
    logger.info("Program started")
    process_data()
    train()
    logger.info("Program finished")


#### src/model_training/trainer.py ####
import logging

logger = logging.getLogger(__name__)


def train():
    """Dummy training function"""
    logger.info("Training model")
    # model training code here
    logger.info("Model training complete")


#### src/data_processing/processor.py ####
import logging

logger = logging.getLogger(__name__)


def process_data():
    """Dummy data processing function"""
    logger.info("Pre-processing data")
    # data preprocessing code here...
    logger.info("Data pre-processing complete")


# -----------


# src/main.py
import logging
import logging.config
import os
from datetime import datetime

from data_processing.processor import process_data
from dotenv import find_dotenv, load_dotenv
from model_training.trainer import train

# find .env file in parent directory
env_file = find_dotenv()
load_dotenv()

CONFIG_DIR = "./config"
LOG_DIR = "./logs"


def setup_logging():
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.ini")
    config_path = "/".join([CONFIG_DIR, config])

    timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
    )


if __name__ == "__main__":

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Program started")
    process_data()
    train()
    logger.info("Program finished")
