from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from config import CHROME_DRIVER_PATH, BASE_URL, USERNAME, PASSWORD, DEFAULT_TIMEOUT
import time

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

    # Wait for login to complete and click on tc01 course
    tc01_course_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='course/view.php?id=2'][data-key='2']"))
    )
    tc01_course_link.click()
        
    grouping_dropdown = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "action-menu-2"))
    )
    grouping_dropdown.click()
    
    # Wait for dropdown menu to appear and click "More..." option
    more_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit settings')]"))
    )
    more_link.click()
    # Wait for the fullname input to be clickable and click it
    fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "id_fullname"))
    )
    fullname_input.send_keys(Keys.CONTROL + "a")  
    fullname_input.send_keys(Keys.DELETE)  
    fullname_input.send_keys("Course Name")
    save_display_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "id_saveanddisplay"))
    )
    save_display_button.click()
    print("✅ ")


except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


