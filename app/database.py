from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = None
Session = scoped_session(sessionmaker())
Base = declarative_base()


def init_db(uri):
    global engine
    engine = create_engine(uri, echo=True)
    Session.configure(bind=engine)


def get_session():
    return Session()


def create_all():
    Base.metadata.create_all(bind=engine)


def shutdown_session(exception=None):
    session = get_session()
    if session:
        session.close()
