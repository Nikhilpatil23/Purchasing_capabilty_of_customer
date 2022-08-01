import joblib
import pandas as pd
import numpy as np
from Logging.setup_logger import setup_logger

# setting up logs
log = setup_logger(logger_name='model_logs', log_file='Logs\Prediction_logs.log')


# creating class for predictions
class Predict:
    def __init__(self, model_path):
        self.model_path = model_path  # path to cluster model
        try:
            log.info(f"loading model from {self.model_path}")
            self.cluster_model = joblib.load(self.model_path)
            log.info('Cluster model loaded')
        except Exception as e:
            log.error('error occured while loading model')
            log.error(e)

    def cluster_predict(self, data):
        try:
            log.info('Predicting cluster for data')
            cluster = self.cluster_model.predict(data)
            log.info(f'Predicted cluster is {cluster}')
            return cluster  # returns cluster number
        except Exception as e:
            log.error('Error occured while predicting cluster')
            log.error(e)
