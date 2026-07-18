from fastapi import APIRouter, Request, Depends, Query
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
  search: str = Query(default=""),
  status: str ="",
  page: int = Query(default=1),
  db: Session = Depends(get_db),
  ):

    if "user_id" not in request.session:
      return RedirectResponse(
        url="/login",
        status_code=303,
      )
    if search:
       jobs = JobService.search_jobs(
          db,
          request.session["user_id"],
          search,
       )
       total_pages = 1

    elif status:
       jobs = JobService.filter_jobs(
          db,
          request.session["user_id"],
          status,
       )  
       total_pages = 1

    else:
       jobs, total_pages = JobService.get_jobs_paginated(
          db,
          request.session["user_id"],
          page=page,
          per_page=5,
       )
    
    stats = JobService.get_statistics(
       db,
       request.session["user_id"],
    )

    success = request.session.pop("success", None)
    print("SUCCESS =", success)
    
    return templates.TemplateResponse(
      request=request,
      name="dashboard.html",
      context={
        "jobs": jobs,
        "stats": stats,
        "page": page,
        "total_pages": total_pages,
        "search": search,
        "status": status,
        "success": success,
      },
    )
    
 