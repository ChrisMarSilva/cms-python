import logging


def get_logger() -> logging.Logger:
    #FORMAT = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\t %(message)s \n"
    FORMAT = "[%(asctime)s] | %(levelname)7s | %(module)10s | %(funcName)11s | %(lineno)4d | %(message)s"
    TIME_FORMAT = "%Y.%m.%d %I:%M:%S %p"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)  # datefmt=TIME_FORMAT,  FILENAME = 'example/path/log.log'
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(handler)
    return logger




# from fastapi.logger import logger as fastapi_logger
# from logging.handlers import RotatingFileHandler
# import logging
#
# formatter = logging.Formatter("[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
# handler = RotatingFileHandler('logfile.log', backupCount=0)
# logging.getLogger("fastapi")
# fastapi_logger.addHandler(handler)
# handler.setFormatter(formatter)
# fastapi_logger.info('****************** Starting Server *****************')
#
# #logging.basicConfig(filename='mylog.log', encoding='utf-8', level=logging.DEBUG)
