from hashlib import sha256

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer)
    thread = relationship(Thread, foreign_keys='thread.id')
    text = Column(String(500), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'))
    recipient_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<Message: {}>'.format(self.id)


class Thread(Base):
    """
    Object representing a mesage thread. A thread is composed of one to many users.
    """
    id = Column(Integer, primary_key=True)
    messages = relationship(Message)
    participants = 
    def __init__(self, arg):
        super(Thread, self).__init__()
        self.arg = arg
        


engine = create_engine('postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
