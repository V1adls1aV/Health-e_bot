from sql_objects import User, Exception, Connection
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime


class UserEditor:
    engine = create_engine("sqlite:///data/Users_data.db", 
    echo=True, future=True)

    def create_user(self, user_name: str):
        with Session(self.engine) as session:
            user = User(
                user_name=user_name,
                user_creating_date=datetime.now()
            )
            session.add(user)
            session.commit()

    def remove_user(self, user_id: int):
        with Session(self.engine) as session:
            user = session.scalar(
                select(User).where(User.user_id == user_id)
            )

            for con in user.connection:
                session.delete(con)

            session.delete(user)
            session.commit()

    def get_user_id(self, user_name: str) -> int:
        with Session(self.engine) as session:
            return session.scalar(
                select(User.user_id)
                .where(User.user_name == user_name)
            )

    def get_user_exceptions(self, user_id: int) -> list:
        with Session(self.engine) as session:
            return session.scalars(
                select(Exception.exception_name)
                .join(Exception.connection)
                .where(Connection.user_id == user_id)
            ).all()
            
    def create_connection(self, user_id: int, exception_id: int):
        with Session(self.engine) as session:
            session.add(Connection(
                user_id=user_id,
                exception_id=exception_id,
                connection_creating_date=datetime.now()
            ))
            session.commit()

    def remove_connection(self, user_id: int, exception_id: int):
        with Session(self.engine) as session:
            session.delete(session.scalar(
                select(Connection)
                .where(Connection.user_id == user_id)
                .where(Connection.exception_id == exception_id)
            ))
            session.commit()


class ExceptionEditor:
    engine = create_engine("sqlite:///data/Users_data.db", 
    echo=True, future=True)

    def create_exception(self, exception_name: str) -> int:
        with Session(self.engine) as session:
            exception = Exception(
                exception_name=exception_name
            )
            session.add(exception)
            session.commit()
            return exception.exception_id

    def remove_exception(self, exception_id: int):
        with Session(self.engine) as session:
            exception = session.scalar(
                select(Exception)
                .where(Exception.exception_id == exception_id)
            )

            if not exception:
                raise UserConnectionExist()

            session.delete(exception)
            session.commit()

    def get_exception_id(self, exception_name: str) -> int:
        with Session(self.engine) as session:
            return session.scalar(
                select(Exception.exception_id)
                .where(Exception.exception_name == exception_name)
            )

    def get_exception_users(self, exception_id: int) -> list:
        with Session(self.engine) as session:
            return session.scalars(
                select(User.user_name)
                .join(User.connection)
                .where(Connection.exception_id == exception_id)
            ).all()


class UserConnectionExist(BaseException):
    def __init__(self) -> None:
        super().__init__(
            'You have to remove user connections to this exception before deleting it.'
        )
