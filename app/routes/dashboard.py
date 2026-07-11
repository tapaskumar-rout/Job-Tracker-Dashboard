from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.job_service import JobService

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
def dashboard(
  request: Request,
  db: Session = Depends(get_db),
  ):

    if "user_id" not in request.session:
      return RedirectResponse(
        url="/login",
        status_code=303,
      )
    
    jobs = JobService.get_jobs_by_user(
       db,
       request.session["user_id"],
    )
    
    return templates.TemplateResponse(
      request=request,
      name="dashboard.html",
      context={
        "jobs": jobs,
      },
    )