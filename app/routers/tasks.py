from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import SessionDep, verify_api_key
from app.models import Task
from app.schemas import TaskCreate, TaskPublic, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(verify_api_key)],
)

@router.get("/", response_model=list[TaskPublic])
def read_tasks(session: SessionDep):
    tasks_db = session.query(Task).all()
    return tasks_db

@router.post("/", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: SessionDep):
    tasks_db = Task(**task.model_dump())
    session.add(tasks_db)
    session.commit()
    session.refresh(tasks_db)
    return tasks_db

@router.patch("/{id}", response_model=TaskPublic)
def update_task(id: int, task: TaskUpdate, session: SessionDep):
    tasks_db = session.get(Task, id)
    if not tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    for k,v in task.model_dump(exclude_unset=True).items():
        setattr(tasks_db, k, v)

    if "is_completed" in task.model_dump(exclude_unset=True):
        if tasks_db.is_completed:
            tasks_db.completed_at = datetime.now(UTC)
        else:
            tasks_db.completed_at = None

    session.commit()
    session.refresh(tasks_db)
    return tasks_db

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, session: SessionDep):
    tasks_db = session.get(Task, id)
    if not tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(tasks_db)
    session.commit()
    return None

