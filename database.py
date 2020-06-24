from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.environ["DB_USER_AWS"]
pw = os.environ["DB_PW_AWS"]
host = os.environ["DB_HOST_AWS"]
name = os.environ["DB_NAME_AWS"]
port = os.environ["DB_PORT_AWS"]

# postgresql://user:password@host:port/dbname
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{pw}@{host}:{port}/{name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# https://docs.sqlalchemy.org/en/13/orm/session_api.html#session-and-sessionmaker
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#declarative-api
Base = declarative_base()