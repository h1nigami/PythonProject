from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String, nullable=False)
    groups = relationship('Group', back_populates='teacher')
    is_admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.name}')>"


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    teacher_id = Column(BigInteger, ForeignKey('teacher.id'), nullable=False)

    teacher = relationship('Teacher', back_populates='groups')

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"


