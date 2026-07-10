from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
def dashboard(request: Request):

  if "user_id" not in request.session:
    return RedirectResponse(
      url="/login",
      status_code=303,
    )
  
  return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context={
      "username": request.session["username"],
    },
  )