from pydantic import BaseModel, Field
from typing import Optional

class JobCreate(BaseModel):
  company: str = Field(min_length=2, max_length=100)
  job_title: str = Field(min_length=2, max_length=100)
  loaction: Optional[str] = None
  status: str = "Applied"
  notes: Optional[str] = None