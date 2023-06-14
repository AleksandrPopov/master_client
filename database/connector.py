from sqlalchemy import create_engine
from config import PORT_DB, NAME, USER_DB, PASSWORD, HOST_DB

engine = create_engine(f'postgresql+psycopg2://{USER_DB}:{PASSWORD}@{HOST_DB}:{PORT_DB}/{NAME}', echo_pool=True)
