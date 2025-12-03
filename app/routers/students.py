from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db


router = APIRouter(
    prefix="/students",
    tags=["students"]
)


@router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Создает нового студента."""
    return crud.create_student(db, student)


@router.get("/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """Получает информацию о студенте по ID."""
    return crud.get_student(db, student_id, raise_not_found=True)


@router.get("/", response_model=list[schemas.Student])
def read_students(db: Session = Depends(get_db)):
    """Получает список всех студентов."""
    return crud.get_students(db)


@router.delete("/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Удаляет студента по ID."""
    return crud.delete_student(db, student_id)


@router.post("/transfer", response_model=schemas.Student)
def transfer_student(transfer: schemas.Transfer, db: Session = Depends(get_db)):
    """Переводит студента из одной группы в другую."""
    return crud.transfer_student(db, transfer)
