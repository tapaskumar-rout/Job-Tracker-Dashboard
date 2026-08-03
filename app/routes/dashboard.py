from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.services.notification_service import NotificationService

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
  sort: str = Query(default="newest"),
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

    elif sort != "newest":
       jobs = JobService.sort_jobs(
          db,
          request.session["user_id"],
          sort,

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

    notifications = NotificationService.get_notifications(
       db,
       request.session["user_id"],
    )
    print(notifications)
    
    today_jobs = JobService.get_today_followups(
       db,
       request.session["user_id"],
    )

    today_followups = JobService.get_today_followups(
       db,
       request.session["user_id"],
    )

    monthly_stats = JobService.get_monthly_statistics(
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
        "sort" : sort,
        "monthly_stats": monthly_stats,
        "today_followups": today_followups,
        "today_jobs": today_jobs,
        "notifications": notifications,
      },
    )
    
 