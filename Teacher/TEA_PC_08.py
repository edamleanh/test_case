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


    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD + Keys.RETURN)


    tc01_course_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='course/view.php?id=2'][data-key='2']"))
    )
    tc01_course_link.click()

    edit_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'single_button') and contains(text(), 'Turn editing on')]"))
    )
    edit_button.click()
    print("✅ Clicked 'Turn editing on' button.")

    action_menu_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "action-menu-toggle-4"))
    )
    action_menu_btn.click()

# Wait for the 'Hide' link to be present
    hide_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item.editing_moveleft.menu-action.cm-edit-action[data-action='moveleft']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", hide_link)
    try:
        hide_link.click()
    except Exception as click_error:
        driver.execute_script("arguments[0].click();", hide_link)











    
    
except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


