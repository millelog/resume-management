# src/models/cover_letter.py

from pydantic import BaseModel

class CoverLetter(BaseModel):
    content: str