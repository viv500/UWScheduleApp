#imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

options = Options()

# this prevents the window from closing after operating
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# explore page url (where the list of courses are)
url = "https://uwflow.com/explore"

#takes the driver to the home page
driver.get(url)

# this is to allow the page to load. it gives it up to 50 seconds
wait = WebDriverWait(driver, 50)
links = set()

# to find the height of the current webpages body
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # this captures all anchor tags
    elements = driver.find_elements(By.XPATH, "//a[@href]")
    for element in elements:

        # to extract relevant data from the anchor tag. i.e. the actual url to each courses page
        # for example, https://uwflow.com/course/mte262
        links.add(element.get_attribute('href'))

    # scrolling down (using the current webpage height we calculated earlier)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # lmao waits 1 second to make sure stuff loads properly
    time.sleep(1)

    # to see if the new content was loaded
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # exit the loop if no new content

    last_height = new_height

print(f"Total unique links found: {len(links)}")

for link in links:
    print(link) #prints the url to each course page

    driver.get(link) #this line directs u to each course page from the links list

    # Now that are u are in each page, scrape data as needed. u might wanna use beautifulsoup4 here

    #*************************************************************************************************





    #*************************************************************************************************

    time.sleep(1)  # some more time


# Optional: close the driver
# driver.quit()
