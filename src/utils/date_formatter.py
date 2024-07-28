# src/utils/date_formatter.py

from datetime import date

def format_date(d: date) -> str:
    if d is None:
        return "Present"
    return d.strftime("%B %Y")