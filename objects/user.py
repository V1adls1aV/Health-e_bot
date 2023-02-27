from objects.sql_objects import DBUser, DBAdditive, DBConnection
from objects.error_objects import DBConnectionsExistError
from objects.additive import Additive
from data.config import DBPATH, PREMIUMLIMIT, ADDITIVELIMIT

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime


class User:
    __engine = create_engine(DBPATH, future=True)
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id
        with Session(self.__engine) as session:
            user = session.scalar(
                select(DBUser)
                .where(DBUser.chat_id == chat_id)
            )

            if not user:  # Creating user
                user = self._create(session)

            self.user_id = user.user_id
            self._premium = user.premium
            
    def __repr__(self) -> str:
        return f'User(user_id={self.user_id}, chat_id={self.chat_id}, premium={self._premium})'

    def _create(self, session) -> DBUser:
        print(f'{datetime.now()} --- Creating user {self.chat_id}')
        user = DBUser(
            chat_id=self.chat_id,
            premium=False,
            user_creating_date=datetime.now()
            )
        session.add(user)
        session.commit()
        return user

    @classmethod
    def get_chats_ids(cls) -> list[int]:
        print(f'{datetime.now()} --- Getting all chats ids')
        with Session(cls.__engine) as session:
            return session.scalars(
                select(DBUser.chat_id)
            ).all()

    @classmethod
    def get_creating_dates(cls) -> list[int]:
        print(f'{datetime.now()} --- Getting all creating dates')
        with Session(cls.__engine) as session:
            return session.scalars(
                select(DBUser.user_creating_date)
            ).all()

    @staticmethod
    def get_current_user(chat_id: int):
        print(f'{datetime.now()} --- Getting user {chat_id}')
        return User(chat_id)

    @property
    def premium(self) -> bool:
        return self._premium

    @premium.setter
    def premium(self, value: bool) -> None:
        print(f'{datetime.now()} --- Setting premium for {self.chat_id}')
        with Session(self.__engine) as session:
            user = session.scalar(
                select(DBUser)
                .where(DBUser.chat_id == self.chat_id)
            )
            user.premium = value
            self._premium = value
            session.commit()

    def remove(self) -> None:
        print(f'{datetime.now()} --- Removing user {self.chat_id}')
        with Session(self.__engine) as session:
            user = session.scalar(
                select(DBUser)
                .where(DBUser.chat_id == self.chat_id)
            )
            if user.connection:
                raise DBConnectionsExistError()

            session.delete(user)
            session.commit()

    def get_additives_names(self) -> list[str] or None:
        print(f'{datetime.now()} --- Getting additives names for {self.chat_id}')
        with Session(self.__engine) as session:
            return list(map(str, session.scalars(
                select(DBAdditive.additive_name)
                .join(DBAdditive.connection)
                .where(DBConnection.user_id == self.user_id)
            ).all()))
    
    def is_adding_avaliable(self) -> bool:
        print(f'{datetime.now()} --- Checking adding avaliable for {self.chat_id}')
        length = len(self.get_additives_names())
        if self._premium and \
            length < PREMIUMLIMIT or length < ADDITIVELIMIT:
            return True
        return False

    def add_additive(self, additive: Additive) -> None:
        print(f'{datetime.now()} --- Adding connection for {self.chat_id}')
        with Session(self.__engine) as session:
            session.add(DBConnection(
                user_id=self.user_id,
                additive_id=additive.additive_id,
                connection_creating_date=datetime.now()
            ))
            session.commit()

    def del_additive(self, additive: Additive) -> None:
        print(f'{datetime.now()} --- Deleting connection for {self.chat_id}')
        with Session(self.__engine) as session:
            session.delete(session.scalar(
                select(DBConnection)
                .where(DBConnection.user_id == self.user_id)
                .where(DBConnection.additive_id == additive.additive_id)
            ))
            session.commit()
