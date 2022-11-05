from sql_objects import DBUser, DBAdditive, DBConnection
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime
from data.config import DBPATH


class Additive:
    __engine = create_engine(DBPATH, echo=True, future=True)
    def __init__(self, additive_name: str) -> None:
        with Session(self.__engine) as session:
            additive = session.scalar(
                select(DBAdditive)
                .where(DBAdditive.additive_name == additive_name)
            )
            if not additive:
                additive = DBAdditive(
                    additive_name=additive_name
                )
                session.add(additive)
                session.commit()

            self.additive_id = additive.additive_id
            self.additive_name = additive_name

    def __repr__(self) -> str:
        return f'Additive(additive_id={self.additive_id}, additive_name="{self.additive_name}")'

    def remove(self):
        with Session(self.__engine) as session:
            additive = session.scalar(
                select(DBAdditive)
                .where(DBAdditive.additive_id == self.additive_id)
            )

            if additive.connection:
                raise DBConnectionExist()

            session.delete(additive)
            session.commit()


class User:
    __engine = create_engine(DBPATH, echo=True, future=True)
    def __init__(self, chat_id: int) -> None:
        with Session(self.__engine) as session:
            user = session.scalar(
                select(DBUser)
                .where(DBUser.chat_id == chat_id)
            )
            if not user:
                user = DBUser(
                    chat_id=chat_id,
                    user_creating_date=datetime.now()
                )
                session.add(user)
                session.commit()

            self.user_id = user.user_id
            self.chat_id = chat_id

    def __repr__(self) -> str:
        return f'User(user_id={self.user_id}, chat_id={self.chat_id})'

    def remove(self):
        with Session(self.__engine) as session:
            user = session.scalar(
                select(DBUser)
                .where(DBUser.chat_id == self.chat_id)
            )
            if user.connection:
                raise DBConnectionExist()

            session.delete(user)
            session.commit()
    
    @classmethod
    def get_chats_ids(cls) -> list[int]:
        with Session(cls.__engine) as session:
            return session.scalars(
                select(DBUser.chat_id)
            ).all()

    def get_additives(self) -> list[str]:
        with Session(self.__engine) as session:
            return session.scalars(
                select(DBAdditive.additive_name)
                .join(DBAdditive.connection)
                .where(DBConnection.user_id == self.user_id)
            ).all()

    def add_additive(self, additive: Additive):
        with Session(self.__engine) as session:
            session.add(DBConnection(
                user_id=self.user_id,
                additive_id=additive.additive_id,
                connection_creating_date=datetime.now()
            ))
            session.commit()

    def del_additive(self, additive: Additive):
        with Session(self.__engine) as session:
            session.delete(session.scalar(
                select(DBConnection)
                .where(DBConnection.user_id == self.user_id)
                .where(DBConnection.additive_id == additive.additive_id)
            ))
            session.commit()


class DBConnectionExist(BaseException):
    def __init__(self) -> None:
        super().__init__(
            'You have to remove all DB connections before deleting this item.'
        )
