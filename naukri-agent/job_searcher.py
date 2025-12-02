from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time
import random

class JobSearcher:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def random_sleep(self, min_seconds=2, max_seconds=5):
        time.sleep(random.uniform(min_seconds, max_seconds))

    def human_scroll(self):
        # Scroll down a bit randomly
        height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_to = random.randint(0, int(height/2))
        self.driver.execute_script(f"window.scrollTo(0, {scroll_to});")
        self.random_sleep(1, 3)

    def login(self):
        print("Logging in...")
        self.driver.get("https://www.naukri.com/nlogin/login")
        
        try:
            username_field = self.wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
            username_field.send_keys(Config.NAUKRI_USERNAME)
            
            password_field = self.driver.find_element(By.ID, "passwordField")
            password_field.send_keys(Config.NAUKRI_PASSWORD)
            self.random_sleep(1, 2)
            
            login_btn = self.driver.find_element(By.XPATH, "//button[text()='Login']")
            login_btn.click()
            
            # Wait for login to complete (check for profile picture or name)
            # This might fail if CAPTCHA appears
            self.random_sleep(5, 8) 
            if "nlogin" not in self.driver.current_url:
                print("Login successful (likely).")
                return True
            else:
                print("Login failed or CAPTCHA present. Please solve manually.")
                input("Press Enter after solving CAPTCHA and logging in...")
                return True
                
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def search_jobs(self):
        print("Searching for jobs...")
        keywords = "%20".join(Config.KEYWORDS)
        location = Config.LOCATION
        # sort=f sorts by Date (Freshness)
        url = f"https://www.naukri.com/{keywords.lower().replace(' ', '-')}-jobs-in-{location.lower()}?sort=f"
        
        self.driver.get(url)
        self.random_sleep(3, 6)
        self.human_scroll()
        
        job_links = []
        try:
            print(f"Scraping URL: {self.driver.current_url}")
            
            # Strategy 1: Look for specific job tuple classes
            selectors = [
                "div.srp-jobtuple-wrapper", 
                "article.jobTuple", 
                "div.list"
            ]
            
            cards = []
            for sel in selectors:
                cards = self.driver.find_elements(By.CSS_SELECTOR, sel)
                if cards:
                    print(f"Found {len(cards)} cards using selector: {sel}")
                    break
            
            # Strategy 2: If cards found, find links within them
            if cards:
                for card in cards[:5]:
                    try:
                        # Try finding title link
                        link_elem = card.find_element(By.CSS_SELECTOR, "a.title")
                        job_links.append(link_elem.get_attribute("href"))
                    except:
                        continue
            
            # Strategy 3: Direct link search if cards failed
            if not job_links:
                print("Strategy 1 failed. Trying direct link search...")
                links = self.driver.find_elements(By.CSS_SELECTOR, "a.title")
                for link in links[:5]:
                    job_links.append(link.get_attribute("href"))
                    
        except Exception as e:
            print(f"Error scraping jobs: {e}")
            
        return job_links

    def get_job_description(self, url):
        self.driver.get(url)
        self.random_sleep(3, 6)
        self.human_scroll()
        try:
            # Try multiple selectors for JD
            jd_elem = self.driver.find_element(By.CLASS_NAME, "job-desc")
            return jd_elem.text
        except:
            try:
                jd_elem = self.driver.find_element(By.CLASS_NAME, "styles_job-desc-container__txpYf") # New UI
                return jd_elem.text
            except:
                return "Could not extract JD."

if __name__ == "__main__":
    # Test
    pass
