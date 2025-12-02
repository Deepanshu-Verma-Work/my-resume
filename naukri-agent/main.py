from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from job_searcher import JobSearcher
from resume_tailor import ResumeTailor
import time
import random
import os

import csv
from config import Config

def main():
    print("Initializing Naukri AI Agent...")
    
    # Setup Browser
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Disable headless for login visibility
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        searcher = JobSearcher(driver)
        tailor = ResumeTailor()
        
        # 1. Login
        if not searcher.login():
            print("Login failed. Exiting.")
            return

        # 2. Search Jobs
        job_links = searcher.search_jobs()
        print(f"Found {len(job_links)} jobs.")
        
        # Prepare CSV for application tracking
        csv_path = os.path.join(Config.OUTPUT_DIR, "jobs.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Job URL", "Resume Path", "Status"])
            
            for i, link in enumerate(job_links):
                print(f"\nProcessing Job {i+1}: {link}")
                time.sleep(random.uniform(5, 10)) # Human-like pause between jobs
                
                # 3. Get JD
                jd_text = searcher.get_job_description(link)
                if len(jd_text) < 100:
                    print("JD too short or failed to extract. Skipping.")
                    continue
                    
                print("Extracted JD. Tailoring resume...")
                
                # 4. Tailor Resume
                modified_latex = tailor.tailor_resume(jd_text)
                
                if modified_latex:
                    filename = f"tailored_resume_{i+1}.tex"
                    saved_path = tailor.save_resume(modified_latex, filename)
                    print(f"Tailored resume saved to: {saved_path}")
                    
                    # Compile PDF
                    pdf_path = tailor.compile_resume(saved_path)
                    
                    if pdf_path:
                        # Log to CSV
                        writer.writerow([link, saved_path, "Ready to Apply"])
                        f.flush() # Ensure write
                    else:
                        print("Skipping CSV log due to compilation failure.")
                else:
                    print("Failed to tailor resume.")
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
