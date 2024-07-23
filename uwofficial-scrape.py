from Course import Course
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

subject = str(input("Enter subject code (eg. CS, GBDA, AFM): "))
url = str(input("Enter subject course-list catalogue URL: "))


options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

scroll_and_collect_links()

print(f"Total unique links found: {len(links)}")


for link in links:
    try:
        if subject in link:
            driver.get(link)
            time.sleep(3)  # 3 seconds for the page to fully load

            # initialize course class
            course = Course()

            # these specific divs contain description, units, prerequisites, antirequisites, and cross listed courses
            course_name_elements = driver.find_elements(By.XPATH, '//div[@class="course-view__itemTitleAndTranslationButton___36N-_"]')
            if course_name_elements:
                course.title = course_name_elements[0].text

            # find all <h3> elements
            h3_elements = driver.find_elements(By.XPATH, '//h3[@class="course-view__label___FPV12"]')

            for h3 in h3_elements:
                # extract <h3> text
                h3_text = h3.text
                
                # find all children divs within this specific <h3> element
                div_elements = h3.find_elements(By.XPATH, './/following-sibling::div')

                content = []
                for div in div_elements:
                    content.append(div.text)

                # assign attributes of object based on <h3> content
                if "Description" in h3_text:
                    course.description = ' '.join(content)
                elif "Prerequisites" in h3_text:
                    course.prerequisites = ' '.join(content)
                elif "Antirequisites" in h3_text:
                    course.antirequisites = ' '.join(content)
                elif "Cross-Listed Courses" in h3_text:
                    course.crosslisted = ' '.join(content)

            print(course) #the __str__ method in the class takes care of this
            print("\n\n")

    except Exception as e:
        print(f"An error occurred while processing {link}: {e}")

# Optional: close the driver
# driver.quit()
