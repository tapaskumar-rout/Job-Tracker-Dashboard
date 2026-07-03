from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import APP_NAME, APP_VERSION
from app.database.database import Base,engine
import app.models # noqa: F401


from app.routes.home import router as home_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home_router)
