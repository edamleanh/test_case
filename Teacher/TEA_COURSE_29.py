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

    # Wait for the enrolled users page to load
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "usercheckbox"))
    )

    email_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//tr[td[contains(text(), 'student2@gmail.com')]]//input[@type='checkbox']"))
    )
    email_checkbox.click()

    form_action_dropdown = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "formactionid"))
    )
    

    select = Select(form_action_dropdown)
    
    select.select_by_value("bulkchange.php?plugin=manual&operation=deleteselectedusers")

    submit_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "id_submitbutton"))
    )
    submit_button.click()
    print("✅ Successfully clicked 'Unenrol users' button")

    try:
        success_notification = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert.alert-info"))
        )
        
        # Get the notification text
        notification_text = success_notification.text
        print(f"🎉 Success notification detected: {notification_text}")
        
        # Check if it contains unenrolled users message
        if "unenrolled users" in notification_text.lower():
            print("✅ User successfully unenrolled from the course!")
        else:
            print(f"ℹ️ Notification received: {notification_text}")
            
    except Exception as notification_error:
        print(f"⚠️ Could not detect success notification: {notification_error}")

    try:
        close_button = driver.find_element(By.CSS_SELECTOR, ".alert .close")
        close_button.click()
        print("✅ Success notification dismissed")
    except:
        pass  

    



except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


