from objects.error_objects import DBConnectionsExistError
from objects.sql_objects import DBAdditive
from data.config import DBPATH

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


class Additive:
    __engine = create_engine(DBPATH, echo=True, future=True)
    def __init__(self, additive_name: str) -> None:
        self.additive_name = additive_name
        with Session(self.__engine) as session:     
            additive = session.scalar(
                select(DBAdditive)
                .where(DBAdditive.additive_name == additive_name)
            )

            if not additive:
                additive = self._create(session)

            self.additive_id = additive.additive_id

    def __repr__(self) -> str:
        return f'Additive(additive_id={self.additive_id}, additive_name="{self.additive_name}")'

    def _create(self, session) -> DBAdditive:
            additive = DBAdditive(
                    additive_name=self.additive_name
                )
            session.add(additive)
            session.commit()
            return additive

    def remove(self) -> None:
        with Session(self.__engine) as session:
            additive = session.scalar(
                select(DBAdditive)
                .where(DBAdditive.additive_id == self.additive_id)
            )

            if additive.connection:
                raise DBConnectionsExistError()

            session.delete(additive)
            session.commit()
