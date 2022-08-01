import logging

log_format = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'

formatter = logging.Formatter(log_format)

def setup_logger(logger_name = 'my_log',
                 log_file = 'my_log.log',
                 level = logging.DEBUG,
                 log_format = formatter) :
    handler = logging.FileHandler(log_file) #adding logfile to file handler
    handler.setFormatter(log_format) #setting the format for logger

    logger = logging.getLogger(logger_name) #creating the main logger
    logger.setLevel(level) # setting the logger level
    logger.addHandler(handler) #adding the logger to filehandler
    return logger

#log1 = setup_logger(logger_name= 'log1', log_file='log1.log')
#log1.info('testing log1 file')