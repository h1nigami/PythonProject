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
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    @staticmethod
    def create_table():
        Base.metadata.create_all(engine)

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

    def add_admin(self, tg_id:int, name:str, group:Group|None):
        try:
            if group is None:
                admin = Teacher(tg_id, name, is_admin=True)
                self.session.add(admin)
                self.session.commit()
                self.session.close()
            else:
                admin = Teacher(tg_id, name, group, is_admin=True)
                self.session.add(admin)
                self.session.commit()
                self.session.close()
        except:
            self.session.rollback()
        finally:
            self.session.close()

    def is_admin(self, tg_id:int)->bool:
        teacher = self.session.query(Teacher).get(tg_id)
        if teacher.is_admin:
            return True
        else:
            return False


db = DataBase()
