import requests
from bs4 import BeautifulSoup

def fetch_jobs(level="entry"):
    query = "entry level" if level == "entry" else "experienced"
    url = f"https://in.indeed.com/jobs?q={query}&l=India"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    for card in soup.select(".job_seen_beacon")[:20]:
        title = card.select_one("h2 span")
        company = card.select_one(".companyName")
        link = card.select_one("a")

        if title and company and link:
            jobs.append({
                "title": title.text,
                "company": company.text,
                "apply_link": "https://in.indeed.com" + link["href"]
            })

    return jobs
