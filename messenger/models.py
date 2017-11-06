from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class Thread(Base):
    """
    Object representing a mesage thread. A thread is composed of one to many users.
    """
    __tablename__ = "thread"
    pk = Column(Integer, primary_key=True)
    messages = relationship("Message")
    participants = Column(ARRAY(Integer))

    def __init__(self, participants):
        super(Thread, self).__init__()
        self.participants = participants


class Message(Base):
    """
    Object model for a message. Messages are attached to a thread via a FK. All participants of a thread recive the
    message.
    """
    __tablename__ = "message"
    pk = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey("thread.pk"))
    text = Column(String(500), nullable=False)
    sender_id = Column(Integer)


engine = create_engine('postgresql+psycopg2://admin:admin@db:5432/messenger')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
