from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.dashboard import router as dashboard_router
from starlette.middleware.sessions import SessionMiddleware
from app.routes.jobs import router as jobs_router


from app.core.config import APP_NAME, APP_VERSION
from app.database.database import Base,engine
import app.models # noqa: F401


from app.routes.home import router as home_router
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

app.add_middleware(
  SessionMiddleware,
  secret_key="job_tracker_secret_2026"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.mount(
  "/company_logos",
  StaticFiles(directory="company_logos"),
  name="company_logos",
)

app.mount(
  "/uploads",
  StaticFiles(directory="uploads"),
  name="uploads"
)

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(jobs_router)
