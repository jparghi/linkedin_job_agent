# LinkedIn Job Search Agent (Updated)

Automates LinkedIn job searches using Playwright with saved login session, dynamic scrolling, and updated selectors.

## ✅ Features
- Manual login once — session is saved
- Reuses saved session on future runs
- Scrolls the job listing page to load more jobs
- Scrapes job title, company, location, and link
- Saves job data to `~/Documents/job_search_agent/linkedin_jobs.csv`

## 🛠 Setup

python3 -m venv venv
source venv/bin/activate


1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

2. Run the script:
```bash
python linkedin_scraper.py
```

3. First run will ask you to log into LinkedIn. Future runs will reuse the saved session.

Enjoy!
