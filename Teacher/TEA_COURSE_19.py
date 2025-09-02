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

    grouping_dropdown = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "displaydropdown"))
    )
    grouping_dropdown.click()
    
    
    # Wait for dropdown menu to appear and click "Removed from view"
    removed_from_view_option = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dropdown-item[data-display-option='display'][data-value='summary']"))
    )
    removed_from_view_option.click()
        
    print("✅")

except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


