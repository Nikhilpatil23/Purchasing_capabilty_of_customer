#creating the class to scale the data
import joblib
from Logging.setup_logger import  setup_logger
import pandas as pd
import numpy as np

#setting up logs

log = setup_logger(logger_name= 'scaler_logs', log_file='Logs\Scaling_logs.log')

class Scaler :
    def __init__(self, scaler_model_path):
        try :
            log.info('Initialising scaling class')
            self.scaler_model_path = scaler_model_path

            #Loading scaler model
            log.info('Loading scaler model')
            self.scalemodel = joblib.load(self.scaler_model_path)
            self.scalemodel.clip = False
            log.info('scaler model loaded successfully')

        except Exception as e :
            log.error('Error in initialising scaler class')
            log.error(e)

    def scale_data(self,data): #scaling the data
        try :
            if isinstance(data,np.ndarray) : #checking if the input data is array or not
                log.info('data is valid')
                log.info('scaling the data')
                data_scaled = self.scalemodel.transform(data)
                log.info('Scaling of numpy array done ')
                return data_scaled
            else :
                log.error('data is invalid')
                raise ValueError('data is invalid')
        except Exception as e :
            log.error('Error in scaling numpy array')
            log.error(e)



