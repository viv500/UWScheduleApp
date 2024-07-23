from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://uwflow.com/explore"
driver.get(url)

wait = WebDriverWait(driver, 50)
links = set()

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    elements = driver.find_elements(By.XPATH, "//div[@role='cell']//a[@href]")
    for element in elements:
        links.add(element.get_attribute('href'))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

    last_height = new_height

print(f"Total unique links found: {len(links)}")
print(links)
course_data_list = []

for link in links:
    driver.get(link)

    try:
        title_class = 'sc-pktCe eHAbVk'
        print(f"Processing link: {link}")
        
        #xpaths
        prereq_xpath = "//div[@class='sc-ptdsS hxDuVK']"
        coreq_xpath = "//div[@class='sc-pkIrX fqDIne']"
        antireq_xpath = "//div[@class='sc-ptdsS hxDuVK']"

        #waiting for those elements to load
        prereq_element = wait.until(EC.presence_of_element_located((By.XPATH, prereq_xpath)))
        coreq_element = wait.until(EC.presence_of_element_located((By.XPATH, coreq_xpath)))
        antireq_element = wait.until(EC.presence_of_element_located((By.XPATH, antireq_xpath)))

        #print(f"Link: {link}")

        # extracting course name from url
        print(f"Course: {link[26:]}")
        print(f"Prerequisites: {prereq_element.text}")
        print(f"Corequisites: {coreq_element.text}")
        print(f"Antirequisites: {antireq_element.text}")
        print(" ")


    except Exception as e:
        print(f"An error occurred while scraping {link}: {e}")

    time.sleep(1)

# Optional: close the driver
# driver.quit()

print(f"Total courses scraped: {len(course_data_list)}")
