from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def create_item(db, item, model):
    """Создает элемент в базе данных."""
    db_item = model(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_item(db, item_id, model, not_found_detail=None):
    """Получает элемент по ID или вызывает исключение, если не найден."""
    item = db.query(model).filter(model.id == item_id).first()

    if not item and not_found_detail:
        raise HTTPException(status_code=404, detail=not_found_detail)

    return item


def get_items(db, model):
    """Получает список всех элементов модели."""
    return db.query(model).all()


def delete_item(db, item_id, model, not_found_detail):
    """Удаляет элемент по ID после проверки на существование."""
    db_item = get_item(db, item_id, model, not_found_detail)
    db.delete(db_item)
    db.commit()

    return db_item


def create_student(db, student):
    """Создает нового студента."""
    return create_item(db, student.model_dump(), models.Student)


def get_student(db, student_id, raise_not_found=False):
    """Получает студента по ID."""
    not_found_detail = "Student not found" if raise_not_found else None

    return get_item(db, student_id, models.Student, not_found_detail)


def get_students(db):
    """Получает список всех студентов."""
    return get_items(db, models.Student)


def delete_student(db, student_id):
    """Удаляет студента по ID."""
    return delete_item(db, student_id, models.Student, "Student not found")


def create_group(db, group):
    """Создает новую группу."""
    return create_item(db, group.model_dump(), models.Group)


def get_group(db, group_id, raise_not_found=False):
    """Получает группу по ID."""
    not_found_detail = "Group not found" if raise_not_found else None

    return get_item(db, group_id, models.Group, not_found_detail)


def get_groups(db):
    """Получает список всех групп."""
    return get_items(db, models.Group)


def delete_group(db, group_id):
    """Удаляет группу по ID."""
    return delete_item(db, group_id, models.Group, "Group not found")


def add_student_to_group(db, group_id, student_id):
    """Добавляет студента в группу."""
    student = get_student(db, student_id, raise_not_found=True)
    group = get_group(db, group_id, raise_not_found=True)

    if student.group_id == group_id:
        raise HTTPException(
            status_code=400,
            detail="Student already in group"
        )

    student.group_id = group_id
    db.commit()
    db.refresh(student)

    return student


def remove_student_from_group(db, group_id, student_id):
    """Удаляет студента из группы."""
    student = get_student(db, student_id, raise_not_found=True)

    if student.group_id != group_id:
        raise HTTPException(
            status_code=400,
            detail="Student not in this group"
        )

    student.group_id = None
    db.commit()
    db.refresh(student)

    return student


def get_students_in_group(db, group_id):
    """Получает список студентов в группе."""
    get_group(db, group_id, raise_not_found=True)

    return (
        db.query(models.Student)
        .filter(models.Student.group_id == group_id)
        .all()
    )


def transfer_student(db, transfer):
    """Переводит студента из одной группы в другую."""
    student = get_student(db, transfer.student_id, raise_not_found=True)

    if student.group_id != transfer.from_group_id:
        raise HTTPException(
            status_code=400,
            detail="Student not in the specified from group"
        )

    to_group = get_group(db, transfer.to_group_id, raise_not_found=True)
    student.group_id = transfer.to_group_id
    db.commit()
    db.refresh(student)

    return student
