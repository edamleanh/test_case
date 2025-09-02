from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from config import CHROME_DRIVER_PATH, BASE_URL, USERNAME, PASSWORD, DEFAULT_TIMEOUT,ID_PROBLEMS,TEST_ACCOUNTS,TEST_QUESTION
import time
import re
import threading


def login_test(account_index, username, password):
    def create_programming_contest_problem(id, name, description, file_path, type_id, language_id):
        # Wait for the 'Add' span and click it
        add_span = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.add-menu"))
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
        fullname_input.send_keys(id)

        fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_name"))
        )
        fullname_input.send_keys(name)  
        
        fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_descriptioneditable"))
        )
        fullname_input.send_keys(description)  

        new_types_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_types_" + str(type_id))) 
        )
        new_types_checkbox.click()

        new_languages_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_languages_" + str(language_id)))
        )
        new_languages_checkbox.click()

        choose_file_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.fp-btn-choose[value='Choose a file...']"))
        )
        choose_file_button.click()

        file_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][name='repo_upload_file']"))
        )
        file_input.send_keys(file_path)
        
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
    driver = None
    try:
        print(f"🚀 Thread {account_index + 1}: Starting login test for {username}")
        
        # Setup WebDriver
        service = EdgeService(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        
        # Open Moodle site
        driver.get(BASE_URL)
        print(f"✅ Thread {account_index + 1}: Opened {BASE_URL}")
        
        # Click login link
        login_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
        )
        login_button.click()
        print(f"✅ Thread {account_index + 1}: Clicked login button")
        
        # Enter credentials
        username_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        
        username_input.send_keys(username)
        password_input.send_keys(password + Keys.RETURN)
        print(f"✅ Thread {account_index + 1}: Entered credentials for {username}")
        
        # Check if login successful
        try:
            WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Dashboard"))
            )
            print(f"🎉 Thread {account_index + 1}: LOGIN SUCCESSFUL for {username}")
            
        except Exception as login_error:
            print(f"❌ Thread {account_index + 1}: LOGIN FAILED for {username} - {login_error}")
        
            
    except Exception as e:
        print(f"💥 Thread {account_index + 1}: ERROR for {username} - {e}")

    driver.get(BASE_URL + "/course/view.php?id="+ str(account_index + 8))

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
    
    edit_progcontest_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'single_button') and contains(text(), 'Edit progcontest')]"))
    )
    edit_progcontest_button.click()
    print("✅ Clicked 'Edit progcontest' button.")
    # Lấy dữ liệu từ TEST_QUESTION trong config.py
    id = ID_PROBLEMS
    for question in TEST_QUESTION:
        problem_id = str(account_index + 1) + id
        problem_name = question.get("name", "question1")
        problem_description = question.get("description", "Description test")
        problem_file_path = question.get("file_path", r"C:\\Users\\edaml\\Downloads\\test_data_1.zip")
        problem_type_id = question.get("type_id", 1)
        problem_language_id = question.get("language_id", 8)
        create_programming_contest_problem(
            id=problem_id,
            name=problem_name,
            description=problem_description,
            file_path=problem_file_path,
            type_id=problem_type_id,
            language_id=problem_language_id
        )
        match = re.search(r"(\D+)(\d+)", id)
        if match:
            prefix = match.group(1)
            num = int(match.group(2)) + 1
            id = f"{prefix}{num}"
    time.sleep(30)
def run_parallel_login_tests():
    print("🚀 Starting parallel login tests for 10 accounts...")
    print("=" * 60)
    
    threads = []
    
    # Tạo và start 10 threads
    for i, account in enumerate(TEST_ACCOUNTS):
        username = account["username"]
        password = account["password"]
        
        thread = threading.Thread(
            target=login_test, 
            args=(i, username, password),
            name=f"LoginTest-{username}"
        )
        threads.append(thread)
        thread.start()
        time.sleep(1)
    
    print(f"✅ Started {len(threads)} login test threads")
    print("=" * 60)
    
    # Chờ tất cả threads hoàn thành
    for i, thread in enumerate(threads):
        thread.join()
        print(f"✅ Thread {i + 1} completed")
    
    print("=" * 60)
    print("🎉 All parallel login tests completed!")

if __name__ == "__main__":
    run_parallel_login_tests()
