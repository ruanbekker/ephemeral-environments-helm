import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.database import get_random_fact, init_db
from app.health import router as health_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(health_router)

PR_NUMBER = os.getenv("PR_NUMBER", "local")
VERSION = os.getenv("VERSION", "1.0.0")
COMMIT = os.getenv("COMMIT", "dev")
POD_NAME = os.getenv("POD_NAME", "local-dev")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    env_data = {
        "pr": PR_NUMBER,
        "version": VERSION,
        "commit": COMMIT,
        "pod_name": POD_NAME
    }

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "env": env_data}
    )


@app.get("/fact")
def fact():
    return {
        "fact": get_random_fact(),
        "served_by": POD_NAME
    }
