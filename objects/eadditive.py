from sql_objects import DBEAdditive
from objects.error_objects import IncorrectArgumentsError
from data.config import DBPATH, EADESCRIPTION

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


class EAdditive:
    __engine = create_engine(DBPATH, echo=True, future=True)
    def __init__(self, word) -> None:
        with Session(self.__engine) as session:
            if not word:
                raise IncorrectArgumentsError()
            
            if word[0] == 'е':
                item = session.scalar(
                    select(DBEAdditive)
                    .where(DBEAdditive.e_number == word)
                    )
            else:
                item = session.scalar(
                    select(DBEAdditive)
                    .where(DBEAdditive.e_name == word)
                    )

            if not item:
                raise IncorrectArgumentsError()
            
            self.e_id = item.e_id
            self.e_number = item.e_number
            self.e_name = item.e_name
            self.harm = item.harm
            self.property = item.property
            self.usage = item.usage
            self.influence = item.influence

    def __repr__(self) -> str:
        return f'EAdditive(e_id="{self.e_id}", e_number="{self.e_number}", e_name="{self.e_name}")'

    def get_description(self):  # How get this from Composition and InlineKeyboard?
        return EADESCRIPTION.format(
            self.e_name, self.e_number, self.harm, 
            self.property, self.usage, self.influence
            )

    @classmethod
    def get_e_numbers(cls) -> list[str]:
        with Session(cls.__engine) as session:
            return session.scalars(
                select(DBEAdditive.e_number)
            ).all()

    @classmethod
    def get_e_names(cls) -> list[str]:
        with Session(cls.__engine) as session:
            return session.scalars(
                select(DBEAdditive.e_name)
            ).all()
