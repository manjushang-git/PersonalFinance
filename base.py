from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME = 'OHM' #enter your USERNAME
PASSWORD = 'OHM' #enter your password
HOST = 'localhost' #enter the oracle db host url
PORT = 1521 # enter the oracle port number
SERVICE = 'PER_FIN' # enter the oracle db service name
ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE


engine = create_engine(ENGINE_PATH_WIN_AUTH)
Session = sessionmaker(bind=engine)

Base = declarative_base()