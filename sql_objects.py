from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class DBConnection(Base):
    __tablename__ = 'connections'

    connection_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    exception_id = Column(Integer, ForeignKey('exceptions.exception_id'))
    connection_creating_date = Column(DateTime)

    user = relationship('DBUser', back_populates='connection')
    exception = relationship('DBException', back_populates='connection')

    def __repr__(self) -> str:
        return f'''
        DBConnection(connection_id={self.connection_id!r}, 
        user_id={self.user_id!r}, exception_id={self.exception_id!r}, 
        connection_creating_date={self.connection_creating_date!r})
        '''


class DBException(Base):
    __tablename__ = 'exceptions'

    exception_id = Column(Integer, primary_key=True)
    exception_name = Column(String)

    connection = relationship('DBConnection', back_populates='exception')

    def __repr__(self) -> str:
        return f'''
        DBException(exception_id={self.exception_id!r}, 
        exception_name={self.exception_name!r})
        '''


class DBUser(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    user_creating_date = Column(DateTime)

    connection = relationship('DBConnection', back_populates='user')

    def __repr__(self) -> str:
        return f'''
        DBUser(user_id={self.user_id!r}, chat_id={self.chat_id!r}, 
        user_creating_date={self.user_creating_date!r})
        '''
