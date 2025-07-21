import os
import time
from playwright.sync_api import sync_playwright
from job_saver import save_jobs_to_csv

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Check for saved session
        if os.path.exists("linkedin_state.json"):
            context = browser.new_context(storage_state="linkedin_state.json")
            print("✅ Using saved LinkedIn session.")
        else:
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://www.linkedin.com/login")
            print("🔐 Please log in manually within 30 seconds...")
            page.wait_for_timeout(30000)
            context.storage_state(path="linkedin_state.json")
            print("✅ Login session saved as 'linkedin_state.json'.")

        page = context.new_page()

        # Use a clean search URL
        query = "Java Developer Remote"
        url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
        print(f"🌐 Navigating to: {url}")
        page.goto(url)
        page.wait_for_timeout(10000)

        # Scroll to load jobs
        for _ in range(5):
            page.mouse.wheel(0, 4000)
            time.sleep(2)

        job_cards = page.query_selector_all(".job-card-container--clickable")
        job_list = []

        for job in job_cards:
            try:
                title = job.query_selector("h3").inner_text().strip() if job.query_selector("h3") else ""
                company = job.query_selector("h4").inner_text().strip() if job.query_selector("h4") else ""
                location = job.query_selector(".job-search-card__location").inner_text().strip() if job.query_selector(".job-search-card__location") else ""
                link_elem = job.query_selector("a")
                link = link_elem.get_attribute("href") if link_elem else ""
                job_list.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Link": f"https://www.linkedin.com{link}" if link.startswith("/jobs/") else link
                })
            except Exception as e:
                print(f"⚠️ Error extracting job: {e}")
                continue

        save_jobs_to_csv(job_list)
        browser.close()

if __name__ == "__main__":
    scrape_jobs()
