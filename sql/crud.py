from sqlalchemy.orm import Session

from sql import models, schemas


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id).one_or_none()


def get_tasks(db: Session):
    return db.query(models.Task).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def complete_task(db: Session, task: schemas.Task, is_completed: bool):
    task.is_completed = is_completed
    db.commit()


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    db.delete(db_task)
    db.commit()
    return {"OK": True}
