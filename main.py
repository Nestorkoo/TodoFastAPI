from fastapi import FastAPI
from database import get_session, engine, SessionDep
from models import Base
import uvicorn
import crud, schemas

app = FastAPI(
    title="FastAPI SQLAlchemy Async",
    description="FastAPI with async SQLAlchemy",
    version="0.1"
)


@app.get("/setupdb", tags=["setup"], summary="Setup database")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Database setup successful"}

@app.post('/tasks', tags=["tasks"], summary="Create task") 
async def create_task(todo: schemas.TaskAddSchema, session: SessionDep) -> schemas.TaskAddSchema:
    await crud.create_task(session, todo)
    return {"message": "Task created"}

@app.get('/tasks', tags=["tasks"], summary="Get all tasks")
async def get_tasks(session: SessionDep):
    return await crud.get_tasks(session)

@app.get('/tasks/{task_id}', tags=["tasks"], summary="Get task by id")
async def get_task(task_id: int, session: SessionDep):
    return await crud.get_task(session, task_id)

@app.put('/tasks/{task_id}', tags=["tasks"], summary="Update task by id")
async def update_task(task_id: int, todo: schemas.TaskAddSchema, session: SessionDep):
    return await crud.update_task(session, task_id, todo)

@app.delete('/tasks/{task_id}', tags=["tasks"], summary="Delete task by id")
async def delete_task(task_id: int, session: SessionDep):
    return await crud.delete_task(session, task_id)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
