from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Our mock database (just like the students dictionary)
todos = {}

# The Pydantic model for a Task
class Task(BaseModel):
    title: str
    completed: bool = False  # By default task is not completed
    due_date: Optional[str] = None  # Optional string for the date

# The Pydantic model for updating a Task
class UpdateTask(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None

@app.get("/")
def index():
    return {"message": "Welcome to my To-Do List API"}

@app.get("/get-task/{task_id}")
def get_task(task_id: int = Path(..., description="The ID of the task you want to view", gt=0)):
    if task_id not in todos:
        return {"Error": "Task not found"}
    return todos[task_id]

@app.post("/create-task/{task_id}")
def create_task(task_id: int, task: Task):
    if task_id in todos:
        return {"Error": "Task already exists"}
    
    todos[task_id] = task
    return todos[task_id]

@app.put("/update-task/{task_id}")
def update_task(task_id: int, task: UpdateTask):
    if task_id not in todos:
        return {"Error": "Task not found"}
    
    if task.title is not None:
        todos[task_id].title = task.title
    
    if task.completed is not None:
        todos[task_id].completed = task.completed

    if task.due_date is not None:
        todos[task_id].due_date = task.due_date

    return todos[task_id]

@app.delete("/delete-task/{task_id}")
def delete_task(task_id: int):
    if task_id not in todos:
        return {"Error": "Task not found"}
    
    del todos[task_id]
    return {"Success": "Task deleted!"}
