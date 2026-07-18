from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class JobCreate(BaseModel):
  company: str = Field(min_length=2, max_length=100)
  job_title: str = Field(min_length=2, max_length=100)
  location: Optional[str] = None
  status: str = "Applied"
  notes: Optional[str] = None
  application_date: Optional[date] = None
  priority: str = "Medium"
  resume: Optional[str] = None
  logo: Optional[str] = None