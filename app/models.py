from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    age = Column(Integer, nullable=False)

    group_id = Column(Integer, ForeignKey("groups.id", ondelete="SET NULL"))
    