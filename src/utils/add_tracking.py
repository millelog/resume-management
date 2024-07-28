#src/utils/add_tracking.py
import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def add_tracking_filter(value, portfolio_url, app_specific_info):
    if not app_specific_info or not portfolio_url:
        return value

    # Convert portfolio_url to string if it's a Pydantic URL object
    portfolio_url_str = str(portfolio_url)

    def replace_url(match):
        url = match.group(1)
        if portfolio_url_str in url:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            query['rs'] = [f"{app_specific_info.company.replace(' ', '').lower()}_{app_specific_info.job_title.replace(' ', '').lower()}"]
            new_query = urlencode(query, doseq=True)
            new_url = urlunparse(parsed_url._replace(query=new_query))
            return f'href="{new_url}"'
        return match.group(0)

    pattern = r'href="([^"]*)"'
    return re.sub(pattern, replace_url, value)