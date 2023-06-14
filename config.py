import os
import pytz

TOKEN_MASTER = os.getenv('TOKEN_MASTER')
TOKEN_CLIENT = os.getenv('TOKEN_CLIENT')

PORT_MASTER = os.getenv('PORT_MASTER')
PORT_CLIENT = os.getenv('PORT_CLIENT')

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
CERT = os.getenv('CERT')

HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')
USER_DB = os.getenv('USER_DB')
NAME = os.getenv('NAME_DB')
PASSWORD = os.getenv('PASSWORD')

COUNTS_MASTERS = int(os.getenv('COUNTS_MASTERS'))
COUNTRY = os.getenv('COUNTRY')

TZ = pytz.timezone(os.getenv('TZ'))
