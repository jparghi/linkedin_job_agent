import os
import csv
from config import SAVE_DIR

def save_jobs_to_csv(jobs, filename="linkedin_jobs.csv"):
    os.makedirs(SAVE_DIR, exist_ok=True)
    file_path = os.path.join(SAVE_DIR, filename)

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Title", "Company", "Location", "Link"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"✅ Saved {len(jobs)} jobs to {file_path}")
