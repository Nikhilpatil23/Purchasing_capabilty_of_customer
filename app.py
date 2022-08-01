from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np

from Cluster_prediction.prediction import Predict
from data_scaling.scaler import Scaler
from Logging.setup_logger import setup_logger
import warnings
warnings.filterwarnings('ignore')

#setting up logs
log =setup_logger(logger_name='flask_app_log', log_file= '.\Logs\App_logs.log')

#creating instance for class
scaler = Scaler('.\saved_models\\scaler.pkl')
pred = Predict('.\saved_models\\cluster_models.pkl')

#creating flask instance
app = Flask(__name__)

#home page
@app.route('/', methods = ['GET','POST'])
def home() :
    return render_template('index.html')

#Prediction page
@app.route('/predict', methods = ['GET','POST'])
def predict() :
    try :
        log.info('Start taking input from webpage')
        if request.method == 'POST' :
            try :
                log.info('Recieved POST request')
                BALANCE = int(request.form['BALANCE'])
                log.info(f'BALANCE : {BALANCE}')
                BALANCE_FREQUENCY = int(request.form['BALANCE_FREQUENCY'])
                log.info(f"BALANCE_FREQUENCY : {BALANCE_FREQUENCY}")
                PURCHASES = int(request.form['PURCHASES'])
                log.info(f"PURCHASES : {PURCHASES}")
                ONEOFF_PURCHASES = int(request.form['ONEOFF_PURCHASES'])
                log.info(f'ONEOFF_PURCHASES : {ONEOFF_PURCHASES}')
                INSTALLMENTS_PURCHASES = int(request.form['INSTALLMENTS_PURCHASES'])
                log.info(f'INSTALLMENTS_PURCHASES : {INSTALLMENTS_PURCHASES}')
                CASH_ADVANCE = int(request.form['CASH_ADVANCE'])
                log.info(f'CASH_ADVANCE : {CASH_ADVANCE}')
                PURCHASES_FREQUENCY = int(request.form['PURCHASES_FREQUENCY'])
                log.info(f'PURCHASES_FREQUENCY : {PURCHASES_FREQUENCY}')
                ONEOFF_PURCHASES_FREQUENCY = int(request.form['ONEOFF_PURCHASES_FREQUENCY'])
                log.info(f'ONEOFF_PURCHASES_FREQUENCY : {ONEOFF_PURCHASES_FREQUENCY}')
                PURCHASES_INSTALLMENTS_FREQUENCY = int(request.form['PURCHASES_INSTALLMENTS_FREQUENCY'])
                log.info(f"PURCHASES_INSTALLMENTS_FREQUENCY : {PURCHASES_INSTALLMENTS_FREQUENCY}")
                CASH_ADVANCE_FREQUENCY = int(request.form["CASH_ADVANCE_FREQUENCY"])
                log.info("CASH_ADVANCE_FREQUENCY: {}".format(CASH_ADVANCE_FREQUENCY))
                CASH_ADVANCE_TRX = int(request.form["CASH_ADVANCE_TRX"])
                log.info("CASH_ADVANCE_TRX: {}".format(CASH_ADVANCE_TRX))
                PURCHASES_TRX = int(request.form["PURCHASES_TRX"])
                log.info("PURCHASES_TRX: {}".format(PURCHASES_TRX))
                CREDIT_LIMIT = int(request.form["CREDIT_LIMIT"])
                log.info("CREDIT_LIMIT: {}".format(CREDIT_LIMIT))
                PAYMENTS = int(request.form["PAYMENTS"])
                log.info("PAYMENTS: {}".format(PAYMENTS))
                MINIMUM_PAYMENTS = int(request.form["MINIMUM_PAYMENTS"])
                log.info("MINIMUM_PAYMENTS: {}".format(MINIMUM_PAYMENTS))
                PRC_FULL_PAYMENT = int(request.form["PRC_FULL_PAYMENT"])
                log.info("PRC_FULL_PAYMENT: {}".format(PRC_FULL_PAYMENT))
                TENURE = int(request.form["TENURE"])
                log.info("TENURE: {}".format(TENURE))
                log.info("Input taken from webpage")
            except Exception as e :
                log.error(f'Error in taking input from webpage {e}')
                return render_template('error.html', error = 'Error in taking input from webpage')
            log.info('Scaling the data')

            #Making array of data
            data = np.array([[BALANCE,BALANCE_FREQUENCY,PURCHASES,ONEOFF_PURCHASES,
            INSTALLMENTS_PURCHASES,
            CASH_ADVANCE,PURCHASES_FREQUENCY,
            ONEOFF_PURCHASES_FREQUENCY,
            PURCHASES_INSTALLMENTS_FREQUENCY,CASH_ADVANCE_FREQUENCY,
            CASH_ADVANCE_TRX,PURCHASES_TRX,
            CREDIT_LIMIT, PAYMENTS,
            MINIMUM_PAYMENTS,PRC_FULL_PAYMENT,TENURE]])

            #scaling data
            scale_data =scaler.scale_data(data)
            log.info('Data scaling completed')
            log.info("Predicting the cluster")
            clus = int(pred.cluster_predict(scale_data))
            log.info(f'Cluster prediction done and found : {str(clus)}')

            #creating pandas dataframe
            pred_df = pd.DataFrame( ) #empty dataframe
            pred_df['Cluster'] = str(clus) #adding cluster
            #saving the dataframe to csv file
            pred_df.to_csv('Prediction.csv',index = False)

            #giving text to show in html page
            try :
                if clus == 0 :
                    text ='Customer belongs to cluster 0 \n they likely to have HIGH PURCHASE CAPABILITY'
                elif clus == 1 :
                    text = 'Customer belongs to cluster 1 \n they likely to have LOW PURCHASE CAPABILITY'
                elif clus == 2 :
                    text = 'Customer belongs to cluster 0 \n they likely buy items in INSTALLMENTS'
                log.info('Sending the prediction on html page')
                return render_template('results.html', prediction = "Cluster Number : " + str(clus), text = text)
            except Exception as e :
                log.error("Error occured while sending prediction on results.html")
                log.error(e)
                return render_template('results.html',prediction = 'Error occured while sending prediction on results.html')

    except Exception as e :
        log.error('Error occured while predicting :' + str(e))
        return jsonify({'Error': str(e)})


if __name__ == '__main__' :
    app.run(debug = True)


