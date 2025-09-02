from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from config import CHROME_DRIVER_PATH, BASE_URL, USERNAME, PASSWORD, DEFAULT_TIMEOUT,ID_PROBLEMS
import time
import re

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



    driver.get("http://172.29.64.156/moodle311/course/view.php?id=2")

    edit_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'single_button') and contains(text(), 'Turn editing on')]"))
    )
    edit_button.click()
    print("✅ Clicked 'Turn editing on' button.")

    add_activity_span = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'section-modchooser-text') and contains(text(), 'Add an activity or resource')]"))
    )
    add_activity_span.click()
    print("✅ Clicked 'Add an activity or resource' span.")

    progcontest_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-action='add-chooser-option' and .//div[contains(@class,'optionname') and contains(text(),'Programming contest')]]"))
    )
    progcontest_link.click()

    fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "id_name"))
    )
    fullname_input.send_keys("Programming Contest 1")  

    save_display_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "id_submitbutton"))
    )
    save_display_button.click()

    # Wait for the 'Edit progcontest' button and click it
    edit_progcontest_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'single_button') and contains(text(), 'Edit progcontest')]"))
    )
    edit_progcontest_button.click()
    print("✅ Clicked 'Edit progcontest' button.")
    id = ID_PROBLEMS
    def create_programming_contest_problem(id):
        # Wait for the 'Add' span and click it
        add_span = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "action-menu-toggle-3"))
        )
        add_span.click()

        # Wait for the 'a new question' link and click it
        add_question_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dropdown-item.addquestion.menu-action.add-menu[data-action='addquestion']"))
        )
        add_question_link.click()

        programming_radio = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "item_qtype_programming"))
        )
        programming_radio.click()

        # Wait for the 'Add' submit button and click it
        add_submit_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.submitbutton.btn.btn-primary[value='Add']"))
        )
        add_submit_button.click()

        # Wait for the 'problem_mode' select dropdown and click it
        problem_mode_select = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_problem_mode"))
        )
        problem_mode_select.click()
        
        # Select 'Create new problem' option
        select = Select(problem_mode_select)
        select.select_by_value("new")

        # Wait for the 'Expand all' link and click it
        expand_all_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.collapseexpand"))
        )
        expand_all_link.click()

        fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_code"))
        )
        fullname_input.send_keys("Q1")

        fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_name"))
        )
        fullname_input.send_keys("question1")  
        
        fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_descriptioneditable"))
        )
        fullname_input.send_keys("Description test")  

        new_types_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_types_1"))
        )
        new_types_checkbox.click()

        new_languages_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_languages_8"))
        )
        new_languages_checkbox.click()

        choose_file_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.fp-btn-choose[value='Choose a file...']"))
        )
        choose_file_button.click()

        file_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][name='repo_upload_file']"))
        )
        file_input.send_keys(r"C:\\Users\\edaml\\Downloads\\test_data_1.zip")
        
        upload_btn = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fp-upload-btn.btn-primary.btn"))
        )
        upload_btn.click()
        
        checker_select = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='checker']"))
        )
        checker_select.click()
        
        checker_select_obj = Select(checker_select)
        checker_select_obj.select_by_value("standard")
        
        add_testcase_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-secondary[onclick='addTestCase()']"))
        )
        add_testcase_button.click()
        
        save_changes_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary[name='submitbutton'][value='Save changes']"))
        )
        save_changes_button.click()
        print("✅ ADD problem id:", id)

        config_path = "c:\\Users\\edaml\\Tester\\Teacher\\config.py"
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("ID_PROBLEMS"):
                match = re.search(r'"(\w+?)(\d+)"', line)
                if match:
                    prefix = match.group(1)
                    num = int(match.group(2)) + 1
                    lines[i] = f'ID_PROBLEMS = "{prefix}{num}"\n'
        with open(config_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    for _ in range(1):
        create_programming_contest_problem(id)
        match = re.search(r"(\D+)(\d+)", id)
        if match:
            prefix = match.group(1)
            num = int(match.group(2)) + 1
            id = f"{prefix}{num}"
except Exception as e:
    print("❌", e)


# Keep browser open for inspection
input("🔎 Press Enter to close the browser...")


driver.quit()


