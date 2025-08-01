from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import *
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

token = str(os.getenv('token'))

engine = create_engine('sqlite:///database.db')


class DataBase:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def add_teacher(self, tg_id:int, name:str, group:Group):
       try:
            teacher = Teacher(tg_id, name, group)
            self.session.add(teacher)
            self.session.commit()
            self.session.close()
       except:
           self.session.rollback()
       finally:
            self.session.close()


