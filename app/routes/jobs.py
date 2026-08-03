from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import csv, io
import os, shutil, uuid

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

@router.get("/jobs/{job_id}")
def view_job(
   job_id: int,
   request: Request,
   db: Session = Depends(get_db),
):
   if "user_id" not in request.session:
      return RedirectResponse("/login", status_code=303)
   
   job = JobService.get_job_by_id(
      db,
      job_id,
      request.session["user_id"],
   )

   if not job:
      return RedirectResponse("/dashboard", status_code=303)
   
   return templates.TemplateResponse(
      request=request,
      name="job_details.html",
      context={
         "job": job,
      },
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
    application_date: date =Form(...),
    priority: str = Form(...),
    resume: UploadFile = File(None),
    logo: UploadFile = File(None),
    follow_up_date: date | None = Form(None),
):
  
    if "user_id" not in request.session:
       return RedirectResponse(
        url="/login",
        status_code=303,
     )
    
    resume_filename = None
    
    if resume and resume.filename:
       
       if not resume.filename.lower().endswith(".pdf"):
          return RedirectResponse(
             url="/jobs/new",
             status_code=303,
          )
       resume_filename = f"{uuid.uuid4()}.pdf"

       UPLOAD_DIR = "uploads"
       os.makedirs(UPLOAD_DIR, exist_ok=True)

       file_path = os.path.join(UPLOAD_DIR, resume_filename)

       with open(file_path, "wb") as buffer:
          shutil.copyfileobj(resume.file, buffer)

    logo_filename = None

    if logo and logo.filename:
       extension = os.path.splitext(logo.filename)[1]
       logo_filename = f"{uuid.uuid4()}{extension}"

       LOGO_DIR = "company_logos"
       os.makedirs(LOGO_DIR, exist_ok=True)

       with open(os.path.join(LOGO_DIR, logo_filename), "wb") as buffer:
          shutil.copyfileobj(logo.file, buffer)   
       
   
    job = JobCreate(
      company=company,
      job_title=job_title,
      location=location,
      status=status,
      priority=priority,
      notes=notes,
      application_date=application_date,
      follow_up_date=follow_up_date,
      resume=resume_filename,
      logo=logo_filename,
    )

    JobService.create_job(
       db=db,
       job_data=job,
       user_id=request.session["user_id"],
       
    )
    
    request.session["success"] = "Job added successfully!"

    return RedirectResponse(
       url="/dashboard",
       status_code=303,
    )

@router.get("/jobs/{job_id}/edit")
def edit_job_page(
   job_id: int,
   request: Request,
   db:Session = Depends(get_db),
):
   
   if "user_id" not in request.session:
      return RedirectResponse("/login", status_code=303)
   
   job = JobService.get_job_by_id(
      db,
      job_id,
      request.session["user_id"],
   )

   if not job:
      return RedirectResponse("/dashboard", status_code=303)
   
   return templates.TemplateResponse(
      request=request,
      name="edit_job.html",
      context={"job": job},
   )

@router.post("/jobs/{job_id}/edit")
def edit_job(
   job_id: int,
   request: Request,
   company: str = Form(...),
   job_title: str = Form(...),
   location: str = Form(...),
   status: str = Form(...),
   notes: str = Form(""),
   db: Session =Depends(get_db),
   resume : UploadFile = File(None),

):
   
   if "user_id" not in request.session:
      return RedirectResponse("/login", status_code=303)
   
   job = JobService.get_job_by_id(
      db,
      job_id,
      request.session["user_id"],
   )

   if not job:
      return RedirectResponse("/dashboard", status_code=303)
   
   job.company = company
   job.job_title = job_title
   job.location = location
   job.status = status
   job.notes = notes

   if resume and resume.filename:

      # Delete old file if it exists
      if job.resume:
         old_file = os.path.join("uploads", job.resume)
         if os.path.exists(old_file):
            os.remove(old_file)

      # Save new file
      filename = f"{uuid.uuid4()}.pdf"
      filepath = os.path.join("uploads", filename)

      with open(filepath, "wb") as buffer:
         shutil.copyfileobj(resume.file, buffer)

      job.resume = filename         

   JobService.update_job(db, job)

   request.session["success"] = "Job updated successfully!"

   print(request.session)

   return RedirectResponse(
      "/dashboard",
      status_code=303,
   )

@router.post("/jobs/{job_id}/delete")
def delete_job(
   job_id: int,
   request: Request,
   db: Session = Depends(get_db),
):
   
   if "user_id" not in request.session:
      return RedirectResponse(
         "/login",
         status_code=303,
      )
   
   job = JobService.get_job_by_id(
      db,
      job_id,
      request.session["user_id"],
   )

   if not job:
      return RedirectResponse(
         "/dashboard",
         satus_code=303,
      )
   
   JobService.delete_job(db, job)

   request.session["success"] = "Job deleted successfully!"

   return RedirectResponse(
      "/dashboard",
      status_code=303,
   )

@router.get("/jobs/export")
def export_jobs(
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

   output = io.StringIO()

   writer = csv.writer(output)

   writer.writerow([
      "Company",
      "Job Title",
      "Location",
      "Status",
      "Priority",
      "Appliation Date",
      "Notes"
   ])

   for job in jobs:
      writer.writerow([
         job.company,
         job.job_title,
         job.location,
         job.status,
         job.priority,
         job.application_date,
         job.notes,
      ])

   output.seek(0)

   return StreamingResponse(
      iter([output.getvalue()]),
      media_type="text/csv",
      headers={
         "Content-Disposition": "attachment; filename=jobs.csv"
      },
   )   