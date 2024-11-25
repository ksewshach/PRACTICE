from fastapi import APIRouter, Request
from schemas import TaskCreateSchema, TaskUpdateSchema
from models import TaskModel
from sqlalchemy.orm import Session
from database import engine
from sqlalchemy import select, insert

tasks_router = APIRouter(prefix='/api/v1/tasks')


@tasks_router.get('/list')
def get_list_task(request: Request):
    session = Session(engine)
    stmt = select(TaskModel)
    object_db = session.execute(stmt)
    tasks:list = object_db.scalars().all()
    session.close()
    return tasks

@tasks_router.post('/create')
def create_task(request: Request, task: TaskCreateSchema):
    session = Session(engine)
    stmt = insert(TaskModel).values(title=task.title,
                                    description=task.description)
    session.execute(stmt)
    session.commit()
    session.close()
    return task

@tasks_router.put('/list/') 
def update_task(request: Request, task_id: int, task_change: TaskUpdateSchema): 
    session = Session(engine)
    stmt = select(TaskModel).where(TaskModel.id==task_id) 
    object_db = session.execute(stmt)
    print(object_db)
    task = object_db.scalars().first()
    task.title = task_change.title
    task.description = task_change.description
    task.status = task_change.status
    session.merge(task)
    session.commit()
    session.close()
    return task_change

@tasks_router.delete('/delete/')
def delete_task(request: Request, task_id: int):
    session = Session(engine)
    stmt = select(TaskModel).where(TaskModel.id==task_id) 
    object_db = session.execute(stmt)
    task = object_db.scalar()
    session.delete(task)
    session.commit()
    session.close()
    return {'message': f'task id: {task_id} delete'}