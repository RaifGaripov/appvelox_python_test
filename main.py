from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# checks if task in db and return it, if not raise exception
def check_task_and_return(db: Session, task_id: int):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404,
                            detail=f"Task with id = {task_id}, not found!")
    return db_task


# get task from id
@app.get('/tasks/get/{task_id}', response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = check_task_and_return(db, task_id)
    result = jsonable_encoder(db_task)
    return result


# get list of tasks
@app.get('/tasks/')
def get_tasks(db: Session = Depends(get_db)):
    db_tasks = crud.get_tasks(db)
    result = jsonable_encoder(db_tasks)
    return result


# create new task
@app.post('/tasks/create/', response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.create_task(db=db, task=task)
    result = jsonable_encoder(db_task)
    return result


# updates task 'is_completed' field
@app.patch('/tasks/complete/{task_id}')
def complete_task(task_id: int, is_completed: bool,
                  db: Session = Depends(get_db)):
    db_task = check_task_and_return(db, task_id)
    crud.complete_task(db=db, task=db_task, is_completed=is_completed)
    return jsonable_encoder(
        f"Task with id = {task_id}, field 'is_completed' = {is_completed}")


# delete task
@app.delete('/tasks/delete/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    check_task_and_return(db, task_id)
    result = crud.delete_task(db, task_id)
    return result
