# src/models/cover_letter.py

from pydantic import BaseModel
from typing import Optional


class JobSpecificInfo(BaseModel):
    company: str
    job_title: str
    
class CoverLetter(BaseModel):
    content: str
    app_specific_info: Optional[JobSpecificInfo] = None
