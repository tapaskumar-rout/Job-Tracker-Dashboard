from app.services.email_service import EmailService
from urllib.parse import quote
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import secrets

from app.database.database import get_db
from app.schemas.user import UserRegister
from app.services.auth_service import AuthService

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/register")
def register_page(request:Request):
  return templates.TemplateResponse(
    request=request,
    name="register.html",
    context={}
  )

@router.post("/register")
def register_user(
  request:Request,
  username: str = Form(...),
  email: str = Form(...),
  password:str = Form(...),
  confirm_password: str = Form(...),
  db: Session = Depends(get_db),
):
  
  if password != confirm_password:
    return templates.TemplateResponse(
      request=request,
      name="register.html",
      context={
        "message":"passwords do not match."
      },
      status_code=400,
    )
  
  try:
    user = UserRegister(
      username=username,
      email=email,
      password=password,
    )

    AuthService.register(db, user)

    return RedirectResponse(
      url="/login",
      status_code=303,
    )
  
  except ValueError as e:
    return templates.TemplateResponse(
      request=request,
      name="register.html",
      context={
        "message": str(e),
      },
      status_code=400,
    )
  
@router.get("/login")
def login_page(request: Request):
  return templates.TemplateResponse(
    request=request,
    name="login.html",
    context={},
  )

@router.post("/login")
def login(
  request: Request,
  email: str = Form(...),
  password: str = Form(...),
  db: Session = Depends(get_db),
):
  
  user = AuthService.authenticate(
    db,
    email,
    password,
  )

  if not user:
    return templates.TemplateResponse(
      request=request,
      name="login.html",
      context={
        "message": "Invalid email or password"
      },
      status_code=401,
    )
  
  request.session["user_id"] = user.id
  request.session["username"] = user.username

  return RedirectResponse(
    url="/dashboard",
    status_code=303,
  )

@router.get("/logout")
def logout(request: Request):

  request.session.clear()

  return RedirectResponse(
    url="/login",
    status_code=303,
  )

@router.get("/forgot-password")
def forgot_password(request: Request):
  return templates.TemplateResponse(
    request=request,
    name="forgot_password.html",
    context={},
  )

@router.post("/forgot-password")
async def forgot_password(
  request: Request,
  email: str = Form(...),
  db: Session = Depends(get_db),
):
  user = AuthService.get_user_by_email(
    db,
    email,
  )

  if not user:
    request.session["error"] = "Email not found."

  reset_link = f"http://127.0.0.1:8000/reset-password?email={quote(email)}"

  await EmailService.send_reset_email(
    email,
    reset_link,
  )

  request.session["success"] = (
    "Password reset linkhas been sent to your email."
  )



  return RedirectResponse(
    "/login",
    status_code=303,
  )

@router.get("/reset-password")
def reset_password_page(
  request: Request,
  email: str,
):
  
  return templates.TemplateResponse(
    request=request,
    name="reset_password.html",
    context={
      "email": email,
    },
  )

@router.post("/reset-password")
def reset_password(
  request: Request,
  email: str = Form(...),
  password: str = Form(...),
  db: Session = Depends(get_db),
):
  
  success = AuthService.reset_password(
    db,
    email,
    password,
  )

  if not success:
    request.session["error"] = "User not found."

    return RedirectResponse(
      "/forgot-password",
      status_code=303,
    )
  
  request.session["success"] = "Password reset successfully"
  
  return RedirectResponse(
    "/login",
    status_code=303,
  )
 

