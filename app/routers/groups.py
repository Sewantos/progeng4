from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db


router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)


@router.post("/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """Создает новую группу."""
    return crud.create_group(db, group)


@router.get("/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    """Получает информацию о группе по ID."""
    return crud.get_group(db, group_id, raise_not_found=True)


@router.get("/", response_model=list[schemas.Group])
def read_groups(db: Session = Depends(get_db)):
    """Получает список всех групп."""
    return crud.get_groups(db)


@router.delete("/{group_id}", response_model=schemas.Group)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """Удаляет группу по ID."""
    return crud.delete_group(db, group_id)


@router.post("/{group_id}/students/{student_id}", 
             response_model=schemas.Student)
def add_student_to_group(group_id: int, student_id: int, 
                         db: Session = Depends(get_db)):
    """Добавляет студента в группу."""
    return crud.add_student_to_group(db, group_id, student_id)


@router.delete("/{group_id}/students/{student_id}", 
               response_model=schemas.Student)
def remove_student_from_group(group_id: int, student_id: int,
                              db: Session = Depends(get_db)):
    """Удаляет студента из группы."""
    return crud.remove_student_from_group(db, group_id, student_id)


@router.get("/{group_id}/students", response_model=list[schemas.Student])
def read_students_in_group(group_id: int, db: Session = Depends(get_db)):
    """Получает список студентов в группе."""
    return crud.get_students_in_group(db, group_id)
