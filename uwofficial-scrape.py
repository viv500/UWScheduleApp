from Course import Course
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import sqlite3
from sqlite3 import Error
#import openai
#from openai.error import RateLimitError, OpenAIError

#api_key = 'your_new_api_key_here'
#openai.api_key = api_key

# Function to create a SQLite database
def create_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            prerequisites TEXT,
            antirequisites TEXT,
            crosslisted TEXT
        )
        ''')

        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error creating database: {e}")

# Function to insert data into SQLite database
def insert_into_db(course, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute('''
        INSERT INTO courses (title, description, prerequisites, antirequisites, crosslisted)
        VALUES (?, ?, ?, ?, ?)
        ''', (course.title, course.description, course.prerequisites, course.antirequisites, course.crosslisted))

        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error inserting data into database: {e}")

# Function to scroll and collect links
def scroll_and_collect_links(driver):
    links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Collect all <a> tags
        elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'style__item___N3dlN')]//div//h3//div//a[@href]")
        for element in elements:
            links.add(element.get_attribute('href'))

        # Scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new content to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    return links

# Function to process each course page
def process_course_page(driver, link):
    try:
        driver.get(link)
        time.sleep(0.7)  # Wait for the page to fully load

        # Initialize course class
        course = Course()

        # Find course title
        course_name_elements = driver.find_elements(By.XPATH, '//div[@class="course-view__itemTitleAndTranslationButton___36N-_"]')
        if course_name_elements:
            course.title = course_name_elements[0].text

        # Find all <h3> elements
        h3_elements = driver.find_elements(By.XPATH, '//h3[@class="course-view__label___FPV12"]')

        for h3 in h3_elements:
            # Extract <h3> text
            h3_text = h3.text

            # Find all children divs within this specific <h3> element
            div_elements = h3.find_elements(By.XPATH, './/following-sibling::div')

            content = []
            for div in div_elements:
                content.append(div.text)

            # Assign attributes of object based on <h3> content
            if "Description" in h3_text:
                course.description = ' '.join(content)
            elif "Prerequisites" in h3_text:


                #openai failed attempt
                """prompt = '''convert the natural language into a nested list of strings. 'One of CS123, CS455; CS910; all of CS876, 654,MUST BE LEVEL 2A OR HIGHER; MUST BE A COMPUTER SCINECE STUDENT should get converted to [["CS123","CS455"], "CS876", "CS654", "2A", "Student-Computer Science"]]. i dont want any course descriptions, only the course code in there'''
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=150
                    )
                    course.prerequisites = response.choices[0].message.content.strip()

                    course.prerequisites = ' '.join(content)
                except RateLimitError as e:
                    print(f"Rate limit exceeded: {e}")
                    time.sleep(10)  # Wait before retrying
                    continue
                except OpenAIError as e:
                    print(f"OpenAI API error: {e}")
                    continue"""
                

                
                course.prerequisites = ' '.join(content)
            elif "Antirequisites" in h3_text:



                # openai failed attempt
                """prompt = '''convert the natural language into a nested list of strings. 'should not have taken any of CS123, cs456, cs872' should get converted to ["CS123", "CS456", "CS872"]. i dont want any course descriptions, only the course code in there'''
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=150
                    )
                    course.antirequisites = response.choices[0].message.content.strip()
                except RateLimitError as e:
                    print(f"Rate limit exceeded: {e}")
                    time.sleep(10)  # Wait before retrying
                    continue
                except OpenAIError as e:
                    print(f"OpenAI API error: {e}")
                    continue"""
                


                course.antirequisites = ' '.join(content)
            elif "Cross-Listed Courses" in h3_text:
                course.crosslisted = ' '.join(content)

        print(course)  # Output the course details
        print("\n\n")

        return course

    except Exception as e:
        print(f"An error occurred while processing {link}: {e}")
        return None

# Main script
def main():
    url = str(input("Enter subject-list catalogue URL: "))
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 50)
    links = scroll_and_collect_links(driver)

    print(f"Total unique links found: {len(links)}")

    db_path = 'courses.db'
    create_database(db_path)

    All_Courses_Final_List = []

    for link in links:
        course = process_course_page(driver, link)
        if course:
            All_Courses_Final_List.append(course)
            insert_into_db(course, db_path)

    print(All_Courses_Final_List)

    # Optional: close the driver
    driver.quit()

if __name__ == "__main__":
    main()
