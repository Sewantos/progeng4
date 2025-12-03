from pydantic import BaseModel
from typing import Optional


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    model_config = {"from_attributes": True}


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    age: int


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    group_id: Optional[int] = None

    model_config = {"from_attributes": True}


class Transfer(BaseModel):
    student_id: int
    from_group_id: int
    to_group_id: int
    