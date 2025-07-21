import os
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from job_saver import save_jobs_to_csv

SEEN_JOBS_FILE = "seen_jobs.json"

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_jobs(job_ids):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(list(job_ids), f)

def notify(title, body):
    os.system(f'''osascript -e 'display notification "{body}" with title "{title}"' ''')

def scrape_and_notify():
    keywords = ["Java", "Software", "Developer"]
    location = "Canada"
    base_url = "https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords="

    seen_jobs = load_seen_jobs()
    new_jobs = []
    updated_seen = seen_jobs.copy()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        if os.path.exists("linkedin_state.json"):
            context = browser.new_context(storage_state="linkedin_state.json")
        else:
            print("❗ Please run the main scraper first to save login state.")
            return

        page = context.new_page()

        for keyword in keywords:
            search_url = f"{base_url}{keyword.replace(' ', '%20')}&location={location}"
            page.goto(search_url)
            page.wait_for_timeout(8000)
            page.mouse.wheel(0, 3000)
            time.sleep(2)

            job_cards = page.query_selector_all(".job-card-container--clickable")

            for job in job_cards:
                try:
                    job_id = job.get_attribute("data-occludable-job-id")
                    if job_id in seen_jobs:
                        continue

                    title = job.query_selector("h3").inner_text().strip() if job.query_selector("h3") else ""
                    company = job.query_selector("h4").inner_text().strip() if job.query_selector("h4") else ""
                    location = job.query_selector(".job-search-card__location").inner_text().strip() if job.query_selector(".job-search-card__location") else ""
                    link_elem = job.query_selector("a")
                    link = link_elem.get_attribute("href") if link_elem else ""
                    full_link = f"https://www.linkedin.com{link}" if link.startswith("/jobs/") else link

                    new_jobs.append({
                        "Title": title,
                        "Company": company,
                        "Location": location,
                        "Link": full_link
                    })
                    updated_seen.add(job_id)

                except Exception as e:
                    continue

        browser.close()

    if new_jobs:
        print(f"🔔 Found {len(new_jobs)} new jobs!")
        save_jobs_to_csv(new_jobs, filename="linkedin_jobs_notified.csv")
        notify("New Jobs Found!", f"{len(new_jobs)} job(s) posted recently.")
    else:
        print("No new jobs found.")

    save_seen_jobs(updated_seen)

if __name__ == "__main__":
    scrape_and_notify()
