from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.models.job import Job

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/admin")
def admin_dashboard(
  request: Request,
  db: Session = Depends(get_db),
):

  if "user_id" not in request.session:
    return RedirectResponse("/login", status_code=303)

  user = db.query(User).filter(
    User.id == request.session["user_id"]
  ).first()

  if not user.is_admin:
    return RedirectResponse("/dashboard", status_code=303)

  total_users = db.query(User).count()
  total_jobs = db.query(Job).count()

  return templates.TemplateResponse(
    request=request,
    name="admin_dashboard.html",
    context={
      "total_users": total_users,
      "total_jobs": total_jobs,
    },
  )