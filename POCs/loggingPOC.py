# creates logs inside folder Runtimes/logs/filename 
# each log file name is in the form: datetime.filename 
# creates a new log for each run 
# WARNING: it cannot create directory, dont wanna use mkdir module


from pathlib import Path
import logging
import datetime


# logs are in the form "logs/filename/datetime.filename.log"
filename = 'loggingPOC'

# create logger and makes it so that it record any message level
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, encoding='utf-8')


logpath = Path(f'logs/{filename}/{datetime.datetime.now()}.{filename}.log')

# logger handler to sent all to correct path
filehandle = logging.FileHandler(logpath)
logger.addHandler(filehandle)

# some test messages
logger.info('info message')
logger.debug('debug message')
logger.warning('warning message')
logger.error('error message')

logger.info(f'info with variables, path = {logpath}, name = {filename}')