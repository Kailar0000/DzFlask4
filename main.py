from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

from data_base import Task

app = FastAPI()
templates = Jinja2Templates(directory="templates")
tasks = []


@app.post("/", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.get("/", response_class=HTMLResponse)
async def show_tasks(request: Request):
    table = pd.DataFrame([vars(task) for task in tasks]).to_html()

    return templates.TemplateResponse("tasks.html", {"request":request, 'table':table})

@app.get("GET /tasks/{task_id}", response_class=HTMLResponse)
async def show_task(request: Request, task_id: int):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task_id:
            return pd.DataFrame([vars(tasks[i])]).to_html()


@app.put("/user/{task_id}", response_model=Task)
async def put_user(task_id: int, task: Task):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task_id:
            task.id = task_id
            tasks[i] = task
            return task


@app.delete("/delete/{task_id}", response_class=HTMLResponse)
async def delet_user(request: Request, task_id: int):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task_id:
            return pd.DataFrame([vars(tasks.pop(i))]).to_html()