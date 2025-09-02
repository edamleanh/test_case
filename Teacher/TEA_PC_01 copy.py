from concurrent.futures import wait
import random
import time
from numpy import number
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from config import CHROME_DRIVER_PATH, BASE_URL, USERNAME, PASSWORD, DEFAULT_TIMEOUT
import pandas as pd
import threading
import datetime



service = EdgeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)


excel_path = "input2.xlsx" 
try:
    df = pd.read_excel(excel_path)
except Exception as e:
    print(f"❌ Không thể đọc file Excel: {e}")
    driver.quit()
    exit()


success_count = 0  
fail_count = 0     

def run_contest(row, idx):
    global success_count, fail_count
    if ( row["Test"] == "no"):
        return
    try:
        driver = webdriver.Chrome(service=service)
        driver.get(BASE_URL)
        login_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
        )
        login_button.click()
        username_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        username_input.send_keys(row["username"])
        password_input.send_keys(row["password"] + Keys.RETURN)
        course_id = row["course_id"]

        driver.get(BASE_URL + f"/course/view.php?id={course_id}")
        edit_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'single_button') and contains(text(), 'Turn editing on')]"))
        )
        edit_button.click()
        # print("✅ Clicked 'Turn editing on' button.")
        add_activity_span = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'section-modchooser-text') and contains(text(), 'Add an activity or resource')]"))
        )
        add_activity_span.click()
        # print("✅ Clicked 'Add an activity or resource' span.")
        progcontest_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-action='add-chooser-option' and .//div[contains(@class,'optionname') and contains(text(),'Programmingcontest')]]"))
        )
        progcontest_link.click()
        expand_all_link = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.collapseexpand"))
        )
        expand_all_link.click()
        if "contest_name" in row and str(row["contest_name"]).lower() != "nan":
            fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_name"))
            )
            fullname_input.send_keys(row["contest_name"])

        save_display_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.NAME, "submitbutton"))
        )
        save_display_button.click()

        edit_progcontest_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'single_button') and contains(text(), 'Edit progcontest')]"))
        )
        edit_progcontest_button.click()

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

        id = random.randint(0, 9999999)

        fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_code"))
        )
        fullname_input.send_keys(id)

        if "problem_name" in row and str(row["problem_name"]).lower() != "nan":
            fullname_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_new_name"))
            )
            fullname_input.send_keys(row["problem_name"])

        if "problem_description" in row and str(row["problem_description"]).lower() != "nan":
            intro_editor = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_new_descriptioneditable"))
            )
            intro_editor.click()
            intro_editor.send_keys(row["problem_description"])

        # Chọn checkbox Public nếu có trường trong file Excel
        if "public" in row and str(row["public"]).strip() == "1":
            print("public")
            public_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_new_is_public"))
            )
            if not public_checkbox.is_selected():
                public_checkbox.click()

        # Chọn độ khó nếu có trường trong file Excel
        if "difficulty" in row and str(row["difficulty"]).strip() in ["easy", "medium", "hard"]:
            difficulty_select = Select(WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_new_difficulty"))
            ))
            difficulty_select.select_by_value(str(row["difficulty"]).strip())

        # Nhập giới hạn thời gian nếu có trường trong file Excel
        if "time_limit" in row and str(row["time_limit"]).strip() != "" and str(row["time_limit"]).lower() != "nan":
            time_limit_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_new_time_limit"))
            )
            time_limit_input.clear()
            time_limit_input.send_keys(str(row["time_limit"]))

        # Nhập giới hạn bộ nhớ nếu có trường trong file Excel
        if "memory_limit" in row and str(row["memory_limit"]).strip() != "" and str(row["memory_limit"]).lower() != "nan":
            memory_limit_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_new_memory_limit"))
            )
            memory_limit_input.clear()
            memory_limit_input.send_keys(str(row["memory_limit"]))


            # Chọn các loại bài toán (checkboxes) dựa trên cột 'problem_types' trong Excel
        if "problem_types" in row and str(row["problem_types"]).strip() != "" and str(row["problem_types"]).lower() != "nan":
            type_list = [t.strip() for t in str(row["problem_types"]).split(";") if t.strip().isdigit()]
            for type_num in type_list:
                checkbox_id = f"id_new_types_{type_num}"
                try:
                    checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                        EC.element_to_be_clickable((By.ID, checkbox_id))
                    )
                    if not checkbox.is_selected():
                        checkbox.click()
                except Exception as e:
                    print(f"⚠️ Không thể chọn checkbox loại {type_num}: {e}")

                

        if "languages_types" in row and str(row["languages_types"]).strip() != "" and str(row["languages_types"]).lower() != "nan":
            type_list = [t.strip() for t in str(row["languages_types"]).split(";") if t.strip().isdigit()]
            for type_num in type_list:
                checkbox_id = f"id_new_languages_{type_num}"
                try:
                    checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                        EC.element_to_be_clickable((By.ID, checkbox_id))
                    )
                    if not checkbox.is_selected():
                        checkbox.click()
                except Exception as e:
                    print(f"⚠️ Không thể chọn checkbox loại {type_num}: {e}")

        if "test_data" in row and str(row["test_data"]).strip() != "" and str(row["test_data"]).lower() != "nan":
            
            choose_file_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.fp-btn-choose[value='Choose a file...']"))
            )
            choose_file_button.click()
            file_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][name='repo_upload_file']"))
            )
            file_input.send_keys((row["test_data"]))

            upload_btn = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fp-upload-btn.btn-primary.btn"))
            )
            upload_btn.click()

            # Chọn checker từ cột 'checker' trong Excel
        if "checker" in row and str(row["checker"]).strip() != "" and str(row["checker"]).lower() != "nan":
            checker_value = str(row["checker"]).strip()
            try:
                checker_select = Select(WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "id_checker"))
                ))
                checker_select.select_by_value(checker_value)
            except Exception as e:
                print(f"⚠️ Không thể chọn checker '{checker_value}': {e}")
        else:
            checker_select = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='checker']"))
            )
            checker_select.click()
            
            checker_select_obj = Select(checker_select)
            checker_select_obj.select_by_value("standard")


        # Click 'Add Test Case' button as many times as specified in Excel
        add_test_case_count = 0
        if "add_test_case" in row and str(row["add_test_case"]).strip() != "" and str(row["add_test_case"]).lower() != "nan":
            add_test_case_count = int(row["add_test_case"])
        for _ in range(add_test_case_count):
            add_testcase_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-secondary[onclick='addTestCase()']"))
            )
            add_testcase_button.click()
               
        if "test_case_type" in row and str(row["test_case_type"]).strip() in ["C", "S", "E"]:
            try:
                testcase_type_select = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='test_cases[0][type]']"))
                )
                select_obj = Select(testcase_type_select)
                select_obj.select_by_value(str(row["test_case_type"]).strip())
            except Exception as e:
                print(f"⚠️ Không thể chọn test case type: {e}")

                # Set test case points if present in Excel
        if "test_case_points" in row and str(row["test_case_points"]).strip() != "" and str(row["test_case_points"]).lower() != "nan":
            try:
                driver.execute_script("document.querySelector('input[name=\"test_cases[0][points]\"]').value = arguments[0];", str(row["test_case_points"]).strip())
            except Exception as e:
                print(f"⚠️ Không thể đặt test case points: {e}")

        if "checker_precision" in row and str(row["checker_precision"]).strip() != "" and str(row["checker_precision"]).lower() != "nan":
            try:
                precision_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "id_checker_precision"))
                )
                precision_input.clear()
                precision_input.send_keys(str(int(row["checker_precision"])))
            except Exception as e:
                print(f"⚠️ Không thể đặt checker precision: {e}")

            # Set output limit if present in Excel
        if "output_limit" in row and str(row["output_limit"]).strip() != "" and str(row["output_limit"]).lower() != "nan":
            try:
                output_limit_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "id_output_limit"))
                )
                output_limit_input.clear()
                output_limit_input.send_keys(str(row["output_limit"]))
            except Exception as e:
                print(f"⚠️ Không thể đặt output limit: {e}")

            # Set output prefix if present in Excel
        if "output_prefix" in row and str(row["output_prefix"]).strip() != "" and str(row["output_prefix"]).lower() != "nan":
            try:
                output_prefix_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "id_output_prefix"))
                )
                output_prefix_input.clear()
                output_prefix_input.send_keys(str(row["output_prefix"]))
            except Exception as e:
                print(f"⚠️ Không thể đặt output prefix: {e}")

        if "unicode" in row and str(int(row["unicode"])) == "1":
            try:
                driver.execute_script("document.getElementById('id_unicode').checked = true;")
            except Exception as e:
                print(f"⚠️ Không thể chọn Unicode checkbox: {e}")

        if "public" in row and str(int(row["public"])) == "1":
            try:
                driver.execute_script("document.getElementById('id_new_is_public').checked = true;")
            except Exception as e:
                print(f"⚠️ Không thể chọn Public checkbox: {e}")

        if "disable_bigInteger" in row and str(int(row["disable_bigInteger"])) == "1":
            try:
                driver.execute_script("document.getElementById('id_nobigmath').checked = true;")
            except Exception as e:
                print(f"⚠️ Không thể chọn No Big Math checkbox: {e}")
        if "defaultmark" in row and str(row["defaultmark"]).strip() != "" and str(row["defaultmark"]).lower() != "nan":
            try:
                defaultmark_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "id_defaultmark"))
                )
                defaultmark_input.send_keys(Keys.CONTROL + "a")
                defaultmark_input.send_keys(Keys.DELETE)
                defaultmark_input.send_keys(str(row["defaultmark"]))
                defaultmark_input.send_keys(Keys.CONTROL + "a")
                defaultmark_input.send_keys(Keys.DELETE)
                defaultmark_input.send_keys(str(row["defaultmark"]))

            except Exception as e:
                print(f"⚠️ Không thể đặt default mark: {e}")
        save_changes_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary[name='submitbutton'][value='Save changes']"))
        )
        time.sleep(100)
        save_changes_button.click()

        # continue_button = WebDriverWait(driver, 5).until(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, "div.continuebutton a"))
        #     )
        # if continue_button:
        #     continue_button.click()
        if str(row["expected_result"]).lower() == "successful":
            try:
                problem_title = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.ID, "action-menu-toggle-4"))
                )
                if problem_title:
                    print(f"✅ Test case {idx} thành công")
                    success_count += 1
                else:
                    print(f"❌ Test case {idx} thất bại")
                    fail_count += 1
            except Exception:
                print(f"❌ Test case {idx} thất bại")
                fail_count += 1
        else:
            try:
                expected_text = str(row["expected_result"])
                error_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{expected_text}')]")
                if any(error_elements):
                    print(f"✅ Test case {idx} thành công: Hiển thị lỗi '{expected_text}'")
                    success_count += 1
                    driver.quit()
                    return
                else:
                    print(f"❌ Test case {idx} thất bại")
                    fail_count += 1
            except Exception:
                print(f"❌ Test case {idx} thất bại")
                fail_count += 1
        driver.quit()
    except Exception as e:
        print(f"❌ Lỗi ở dòng {idx}: {e}")
        fail_count += 1
        try:
            driver.quit()
        except:
            pass
        return


batch_size = 5
total = len(df)
print(total)
for start in range(0, total, batch_size):
    threads = []
    for idx in range(start, min(start + batch_size, total)):
        if idx == 0:  
            continue
        row = df.iloc[idx]
        if row.isnull().all() or all(str(row[col]).strip() == '' or str(row[col]).lower() == 'nan' for col in df.columns):
            continue
        t = threading.Thread(target=run_contest, args=(row, idx))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
print(f"Tổng số test case thành công: {success_count}")
print(f"Tổng số test case thất bại: {fail_count}")
driver.quit()


