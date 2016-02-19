from hashlib import sha256

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(16), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = sha256(password).hexdigest()

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    @property
    def messages(self):
        return (list(session.query(Message).filter_by(sender=self)) +
                list(session.query(Message).filter_by(recipient=self)))


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship(User, foreign_keys='Message.sender_id')
    recipient = relationship(User, foreign_keys='Message.recipient_id')
    recipient_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<Message Sent By: {}>'.format(self.sender.username)


engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
