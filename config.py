from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

SECRET_KEY = 'development key'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_POOL_RECYCLE = 30
