#slay1url/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

engine = create_engine(get_settings().db_url, connect_args={"check_same_thread":False}) 
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)
Base = declarative_base()