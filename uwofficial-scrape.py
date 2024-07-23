from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

course_count = 1

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/courses?group=Accounting%20and%20Financial%20Management%20(AFM)"
driver.get(url)

wait = WebDriverWait(driver, 50)
links = set()

# Function to scroll and collect links
def scroll_and_collect_links():
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Collect all <a> tags
        elements = driver.find_elements(By.XPATH, "//a[@href]")
        for element in elements:
            links.add(element.get_attribute('href'))

        # Scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new content to load

        new_height = driver.execute_script("return document.body.scrollHeight