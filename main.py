from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime
from sql_objects import User, Exception, Connection


engine = create_engine("sqlite:///data/Users_data.db", echo=True, future=True)

with Session(engine) as session:
    """
    u = User(
        user_name='V4',
        user_creating_date=datetime.now()
    )
    
    e = Exception(
        exception_name='nuts'
    )"""

    c = Connection(
        user_id=session.scalar(select(User.user_id).where(User.user_name == 'V2')),
        exception_id=session.scalar(select(Exception.exception_id).where(Exception.exception_name == 'milk')),
        connection_creating_date=datetime.now()
    )

    session.add(c)
    session.commit()
