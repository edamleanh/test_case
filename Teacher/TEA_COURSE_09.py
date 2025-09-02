from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_DRIVER_PATH, BASE_URL, USERNAME, PASSWORD, DEFAULT_TIMEOUT


# Edge WebDriver setup
service = EdgeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)


# Open your Moodle site
driver.get(BASE_URL)


try:
    # Step 1: Click the "Log in" link
    login_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
    )
    login_button.click()


    # Step 2: Wait for username/password fields
    username_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")


    # Enter credentials
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD + Keys.RETURN)


    # Optional: Confirm login worked by checking for "Dashboard" link
    course_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "My courses"))
    )
    course_button.click()

    intro_course_card = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'card dashboard-card')]//span[contains(text(), 'Intro to Programming')]/ancestor::div[contains(@class, 'card dashboard-card')]"))
    )
    
    # Then find the three dots button within that specific course card
    three_dots_button = intro_course_card.find_element(By.CSS_SELECTOR, "button.coursemenubtn[data-toggle='dropdown']")
    three_dots_button.click()
    
    # Wait for dropdown menu to appear and click "Star this course"
    hide_option = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dropdown-item[data-action='hide-course'][data-course-id='2']"))
    )
    hide_option.click()

     # Wait for page to reload and click on the Grouping dropdown
    grouping_dropdown = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "groupingdropdown"))
    )
    grouping_dropdown.click()
    
    
    # Wait for dropdown menu to appear and click "Removed from view"
    removed_from_view_option = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dropdown-item[data-filter='grouping'][data-value='hidden']"))
    )
    removed_from_view_option.click()

    title_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Intro to Programming"))
    )
    
    print("✅")


except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


