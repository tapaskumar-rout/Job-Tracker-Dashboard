from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

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

  return RedirectResponse(
    url="/dashboard",
    status_code=303,
  )



