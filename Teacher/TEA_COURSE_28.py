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
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'More...')]"))
    )
    more_link.click()

    setting = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Users')]"))
    )
    setting.click()

    enrolled_users = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Enrolled users')]"))
    )
    enrolled_users.click()

    # Wait for enrolled users page to load and click "Enrol users" button
    enrol_users_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Enrol users'].btn.btn-secondary"))
    )
    enrol_users_button.click()
    
    print("✅ Clicked 'Enrol users' button")
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,"//input[@placeholder='Search' and @role='combobox']"))
    )

    input_box.click()
    input_box.send_keys("student") 
    time.sleep(1) 
    input_box.send_keys(Keys.RETURN)
    time.sleep(1) 
    input_box.send_keys(Keys.RETURN) 
    time.sleep(1) 
    input_box.send_keys(Keys.RETURN)
    time.sleep(1) 
    input_box.send_keys(Keys.RETURN)
    time.sleep(1) 
    input_box.send_keys(Keys.RETURN)

    driver.find_element(By.PARTIAL_LINK_TEXT, "Show more...").click()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Show less...").click()
    print("✅ Clicked autocomplete dropdown arrow")

    grouping_dropdown = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "id_roletoassign"))
    )
    grouping_dropdown.click()
    select = Select(grouping_dropdown)
    select.select_by_value("5")
    
    print("✅ Selected role with value 5")
    

    enrol_users_final_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary[data-action='save']"))
    )
    enrol_users_final_button.click()
    
    success_message = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'student4@gmail.com')]"))
    )
    
    print("✅ Success! student4@gmail.com enrollment confirmed")
    print(f"Success message: {success_message.text}")






except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


