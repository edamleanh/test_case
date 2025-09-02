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

    course_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Test Course 01')]"))
    )
    course_link.click()

        # Wait for course page to load and click "Turn editing on" button
    turn_editing_on_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary[title=''][type='submit']"))
    )
    turn_editing_on_button.click()
    
    print("✅ Clicked 'Turn editing on' button")
        
    print("✅")

except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


