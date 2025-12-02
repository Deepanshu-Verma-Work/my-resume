from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from job_searcher import JobSearcher
from config import Config
import csv
import os
import time
import random

def apply_to_jobs():
    print("Initializing Application Bot...")
    csv_path = os.path.join(Config.OUTPUT_DIR, "jobs.csv")
    
    if not os.path.exists(csv_path):
        print("No jobs.csv found. Run main.py first.")
        return

    # Setup Browser
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    searcher = JobSearcher(driver)
    
    try:
        if not searcher.login():
            return

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            jobs = list(reader)

        print(f"Found {len(jobs)} jobs to process.")

        for job in jobs:
            url = job["Job URL"]
            resume_path = job["Resume Path"]
            
            # Check if PDF exists (User must compile .tex to .pdf)
            pdf_path = resume_path.replace(".tex", ".pdf")
            if not os.path.exists(pdf_path):
                print(f"Skipping {url}: PDF not found. Please compile {resume_path} to PDF.")
                continue

            print(f"Applying to: {url}")
            driver.get(url)
            searcher.random_sleep(3, 5)
            
            try:
                # Click Apply Button
                apply_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]")
                apply_btn.click()
                searcher.random_sleep(2, 4)
                
                # Handle Chatbot/Modal Application flow (Simplified)
                # Note: Naukri application flows vary (Chatbot, External Link, Simple Upload)
                # This is a basic implementation for the "Simple Upload" flow.
                
                # Look for file upload input
                upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                upload_input.send_keys(pdf_path)
                print("Uploaded Resume.")
                searcher.random_sleep(2, 3)
                
                # Click Submit/Update
                # submit_btn = driver.find_element(By.XPATH, "//button[text()='Update Resume']")
                # submit_btn.click()
                
                print("Application submitted (Simulated).")
                
            except Exception as e:
                print(f"Failed to apply: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    apply_to_jobs()
