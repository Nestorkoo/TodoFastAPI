from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import TaskModel
from schemas import TaskSchema
from database import SessionDep

async def create_task(session: SessionDep, task: TaskSchema):
    new_task = TaskModel(
        title = task.title,
        description = task.description,
        completed = task.completed
    )
    session.add(new_task)
    await session.commit()
    return f'Task {new_task.id} created'

async def get_tasks(session: SessionDep):
    tasks = await session.execute(select(TaskModel))
    return tasks.scalars().all()

async def get_task(session: SessionDep, task_id: int):
    task = await session.execute(select(TaskModel).filter(TaskModel.id == task_id))
    return task.scalars().first()

async def update_task(session: SessionDep, task_id: int, task: TaskSchema):
    db_task = await get_task(session, task_id)
    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    session.add(db_task)
    await session.commit()
    return f'Task {db_task.id} updated'

async def delete_task(session: SessionDep, task_id: int):
    db_task = await get_task(session, task_id)
    session.delete(db_task)
    await session.commit()
    return f'Task {task_id} deleted'