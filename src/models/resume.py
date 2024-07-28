from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict
from datetime import date

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    github: HttpUrl

class Position(BaseModel):
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    responsibilities: Optional[List[str]] = None

class WorkExperience(BaseModel):
    company: str
    positions: List[Position]
    start_date: date
    end_date: Optional[date]
    location: str
    employment_type: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    graduation_date: date
    location: str
    projects: Optional[List[str]] = None

class Resume(BaseModel):
    personal_info: PersonalInfo
    summary: str
    technical_skills: Dict[str, List[str]]
    work_experience: List[WorkExperience]
    education: Education