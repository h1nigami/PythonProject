from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()


class Teacher(Base):
    """Модель учителя"""
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String, nullable=False)
    groups = relationship(argument='Group', back_populates='teacher')
    is_admin = Column(Boolean, nullable=False, default=False)
    scores = Column(Integer, nullable=False, default=100)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.name}')>"


class Group(Base):
    """Модель группы"""
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    teacher_id = Column(BigInteger, ForeignKey('teachers.tg_id'), nullable=True)

    teacher = relationship('Teacher', back_populates='groups')

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"

class Statistics(Base):
    """Статистика по месяцам"""
    __tablename__ = 'statistics'

    teacher_name = Column(String, nullable=False, primary_key=True, unique=False)
    month = Column(Integer, nullable=False, unique=False)
    score = Column(Integer, nullable=False,unique=False)

    def __repr__(self):
        f"<Statistics(teacher_name={self.teacher_name}, month={self.month}, score={self.score})>"


