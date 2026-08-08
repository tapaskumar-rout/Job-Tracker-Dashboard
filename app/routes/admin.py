
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

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

    # Check login
    if "user_id" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    # Get current user
    user = db.query(User).filter(
        User.id == request.session["user_id"]
    ).first()

    if not user:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    # Check admin
    if not user.is_admin:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    # Get all users and jobs
    users = db.query(User).all()
    jobs = db.query(Job).all()

    # Job status statistics
    status_counts = (
        db.query(
            Job.status,
            func.count(Job.id)
        )
        .group_by(Job.status)
        .all()
    )

    status_labels = []
    status_values = []

    for status, count in status_counts:
        status_labels.append(status)
        status_values.append(count)

    total_users = len(users)
    total_jobs = len(jobs)

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "total_users": total_users,
            "total_jobs": total_jobs,
            "users": users,
            "jobs": jobs,
            "status_labels": status_labels,
            "status_values": status_values,
        },
    )


@router.post("/admin/users/{user_id}/delete")
def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
):

    # Check login
    if "user_id" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    # Get current admin
    admin = db.query(User).filter(
        User.id == request.session["user_id"]
    ).first()

    # Check admin permission
    if not admin or not admin.is_admin:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    # Find user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user:

        # Don't allow admin to delete themselves
        if user.id != admin.id:

            # Delete user's jobs first
            db.query(Job).filter(
                Job.user_id == user.id
            ).delete()

            # Delete user
            db.delete(user)

            db.commit()

    return RedirectResponse(
        "/admin",
        status_code=303
    )

