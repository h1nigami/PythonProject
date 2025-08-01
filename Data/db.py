from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///database.db')


class DataBase:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

   def add_teacher(self, tg_id:int, name:str, group:Group):
       try:
            teacher = Teacher(tg_id, name, group)
            self.Session.add(teacher)
            self.Session.commit()
            self.Session.close()
       except:
           self.Session.rollback()
       finally:
            self.Session.close()


