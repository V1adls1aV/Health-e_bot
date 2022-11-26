from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class DBConnection(Base):
    __tablename__ = 'connections'

    connection_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    additive_id = Column(Integer, ForeignKey('additives.additive_id'))
    connection_creating_date = Column(DateTime)

    user = relationship('DBUser', back_populates='connection')
    additive = relationship('DBAdditive', back_populates='connection')

    def __repr__(self) -> str:
        return f'''
        DBConnection(connection_id={self.connection_id!r}, 
        user_id={self.user_id!r}, additive_id={self.exception_id!r}, 
        connection_creating_date={self.connection_creating_date!r})
        '''


class DBAdditive(Base):
    __tablename__ = 'additives'

    additive_id = Column(Integer, primary_key=True)
    additive_name = Column(String)

    connection = relationship('DBConnection', back_populates='additive')

    def __repr__(self) -> str:
        return f'''
        DBAdditive(additive_id={self.additive_id!r}, 
        additive_name={self.additive_name!r})
        '''


class DBEAdditive(Base):
    __tablename__ = 'e_additives'

    e_id = Column(Integer, primary_key=True)
    e_number = Column(String)
    e_name = Column(String)
    harm = Column(String)
    property = Column(String)
    usage = Column(String)
    influence = Column(String)

    def __repr__(self) -> str:
        return f'''
        DBEAdditive(e_id={self.e_id!r}, e_number={self.e_number!r}, e_name={self.e_name!r},
        harm=..., property=..., usage=..., influence=...)
        '''


class DBUser(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    premium = Column(Boolean)
    user_creating_date = Column(DateTime)

    connection = relationship('DBConnection', back_populates='user')

    def __repr__(self) -> str:
        return f'''
        DBUser(user_id={self.user_id!r}, chat_id={self.chat_id!r}, 
        premium={self.premium!r}, user_creating_date={self.user_creating_date!r})
        '''
