from objects.sql_objects import DBECode
from data.config import DBPATH, ECODEDESCRIPTION

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime


class ECode:
    __engine = create_engine(DBPATH, future=True)
    def __init__(self, e_number: str) -> None:
        with Session(self.__engine) as session:
            item = session.scalar(
                select(DBECode)
                .where(DBECode.e_number == e_number)
                )

            if not item:
                return None
            
            self.e_id = item.e_id
            self.e_number = item.e_number
            self.e_name = item.e_name
            self.harm = item.harm
            self.harm_degree = item.harm_degree
            self.feature = item.feature
            self.usage = item.usage
            self.influence = item.influence

    def __repr__(self) -> str:
        return f'''
        ECode(e_id="{self.e_id}", e_number="{self.e_number}", 
        e_name="{self.e_name}", harm_degree={self.harm_degree})
        '''

    def get_description(self):
        print(f'{datetime.now()} --- Making description for {self.e_number}')
        return ECODEDESCRIPTION.format(
            e_name=self.e_name.capitalize(), e_number=self.e_number, harm=self.harm, 
            feature=self.feature, influence=self.influence
            )

    @classmethod
    def get_ecodes(cls) -> dict[str]:
        with Session(cls.__engine) as session:
            res = {}
            ecodes = session.scalars(
                select(DBECode)
            ).all()

            for ecode in ecodes:  # Making the dict
                res[ecode.e_name] = ecode.e_number
            return res
    
    @classmethod
    def get_harm_degree(cls, e_num: str) -> int:
        with Session(cls.__engine) as session:
            return session.scalar(
                select(DBECode.harm_degree)
                .where(DBECode.e_number == e_num)
            )
