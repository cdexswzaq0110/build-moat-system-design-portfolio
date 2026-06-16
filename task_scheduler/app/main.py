from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .routes import router
from .scheduler import initialize_database
from .ui import HOME_HTML


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


initialize_database()
app = FastAPI(title="Task Scheduler", lifespan=lifespan)
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def serve_home() -> HTMLResponse:
    return HTMLResponse(HOME_HTML)
