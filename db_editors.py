from sql_objects import DBUser, DBException, DBConnection
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime
from data.config import DBPATH


class User:
    engine = create_engine(DBPATH, echo=True, future=True)
    def __init__(self, chat_id: int) -> None:
        with Session(self.engine) as session:
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

    @classmethod
    def get_all_chats_ids(cls):
        with Session(cls.engine) as session:
            return session.scalars(
                select(DBUser.chat_id)
            ).all()

    def remove(self):
        with Session(self.engine) as session:
            user = session.scalar(
                select(DBUser)
                .where(DBUser.chat_id == self.chat_id)
            )
            if user.connection:
                raise DBConnectionExist()

            session.delete(user)
            session.commit()

    def get_exceptions(self) -> list:
        with Session(self.engine) as session:
            return session.scalars(
                select(DBException.exception_name)
                .join(DBException.connection)
                .where(DBConnection.user_id == self.user_id)
            ).all()

            
    def create_connection(self, exception: UserException):
        with Session(self.engine) as session:
            session.add(DBConnection(
                user_id=self.user_id,
                exception_id=exception.exception_id,
                connection_creating_date=datetime.now()
            ))
            session.commit()

    def remove_connection(self, exception: UserException):
        with Session(self.engine) as session:
            session.delete(session.scalar(
                select(DBConnection)
                .where(DBConnection.user_id == self.user_id)
                .where(DBConnection.exception_id == exception.exception_id)
            ))
            session.commit()


class UserException:
    engine = create_engine(DBPATH, echo=True, future=True)
    def __init__(self, exception_name: str) -> None:
        with Session(self.engine) as session:
            exception = session.scalar(
                select(DBException)
                .where(DBException.exception_name == exception_name)
            )
            if not exception:
                exception = DBException(
                    exception_name=exception_name,
                    user_creating_date=datetime.now()
                )
                session.add(exception)
                session.commit()

            self.exception_id = exception.exception_id
            self.excepiton_name = exception_name

    def __repr__(self) -> str:
        return f'UserException(exception_id={self.exception_id}, exception_name={self.excepiton_name})'

    def remove_exception(self):
        with Session(self.engine) as session:
            exception = session.scalar(
                select(DBException)
                .where(DBException.exception_id == self.exception_id)
            )

            if not exception.connection:
                raise DBConnectionExist()

            session.delete(exception)
            session.commit()


class DBConnectionExist(BaseException):
    def __init__(self) -> None:
        super().__init__(
            'You have to remove all DB connections before deleting this item.'
        )
