from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.schemas.job import JobCreate
from app.services.job_service import JobService

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/jobs/new")
def new_job(request: Request):

  if "user_id" not in request.session:
    return RedirectResponse(
      url="/login",
      status_code=303,
    )
  
  return templates.TemplateResponse(
    request=request,
    name="job_form.html",
    context={},
  )

@router.post("/jobs/new")
def create_job(
    request: Request,
    company: str = Form(...),
    job_title: str = Form(...),
    location: str = Form(""),
    status: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
  
    if "user_id" not in request.session:
       return RedirectResponse(
        url="/login",
        status_code=303,
     )
   
    job = JobCreate(
      company=company,
      job_title=job_title,
      location=location,
      status=status,
      notes=notes,
    )

    JobService.create_job(
       db=db,
       job_data=job,
       user_id=request.session["user_id"],
    )

    return RedirectResponse(
       url="/dashboard",
       status_code=303,
    )

