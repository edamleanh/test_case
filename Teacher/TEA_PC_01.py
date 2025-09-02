from concurrent.futures import wait
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


def parse_timelimite(time_limit_str):
    """
    Chuyển chuỗi như '60 minutes' hoặc '2 hours' thành số giây
    """
    unit_map = {
        "weeks": 604800,
        "week": 604800,
        "days": 86400,
        "day": 86400,
        "hours": 3600,
        "hour": 3600,
        "minutes": 60,
        "minute": 60,
        "seconds": 1,
        "second": 1
    }
    import re
    if not isinstance(time_limit_str, str):
        return 0
    match = re.match(r"(\d+)\s*(\w+)", time_limit_str.strip())
    if match:
        value = int(match.group(1))
        unit = match.group(2).lower()
        seconds = value * unit_map.get(unit, 0)
        return seconds
    return 0

def parse_datetime(dt_str):
    import pandas as pd
    if isinstance(dt_str, pd.Timestamp):
        return dt_str.to_pydatetime()
    if isinstance(dt_str, datetime.datetime):
        return dt_str
    dt_str = str(dt_str).strip().replace('SA', 'AM').replace('CH', 'PM')
    try:
        return datetime.datetime.strptime(dt_str, "%d/%m/%Y %I:%M:%S %p")
    except ValueError:
        try:
            return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(f"Không nhận diện được định dạng ngày giờ: {dt_str}")


service = EdgeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)


excel_path = "input1.xlsx" 
try:
    df = pd.read_excel(excel_path)
except Exception as e:
    print(f"❌ Không thể đọc file Excel: {e}")
    driver.quit()
    exit()


success_count = 0  # Đếm số test case thành công
fail_count = 0     # Đếm số test case thất bại

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
        if "contest_description" in row and str(row["contest_description"]).lower() != "nan":
            intro_editor = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "id_introeditoreditable"))
            )
            intro_editor.click()
            intro_editor.send_keys(row["contest_description"])

        if row["show_description"] == "1":
            showdesc_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_showdescription"))
            )
            showdesc_checkbox.click()

        # Đọc ngày giờ từ file excel
        if "time_open" in row and str(row["time_open"]).lower() != "nat":
            timeopen_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_timeopen_enabled"))
            )
            timeopen_checkbox.click()
            dt = parse_datetime(row["time_open"])
            day_select = Select(driver.find_element(By.ID, "id_timeopen_day"))
            day_select.select_by_value(str(dt.day))
            month_select = Select(driver.find_element(By.ID, "id_timeopen_month"))
            month_select.select_by_value(str(dt.month))
            year_select = Select(driver.find_element(By.ID, "id_timeopen_year"))
            year_select.select_by_value(str(dt.year))
            hour_select = Select(driver.find_element(By.ID, "id_timeopen_hour"))
            hour_select.select_by_value(str(dt.hour))
            minute_select = Select(driver.find_element(By.ID, "id_timeopen_minute"))
            minute_select.select_by_value(str(dt.minute))

        if "time_close" in row and str(row["time_close"]).lower() != "nat":
            timeclose_checkbox = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_timeclose_enabled"))
            )
            timeclose_checkbox.click()
            dt = parse_datetime(row["time_close"])
            day_select = Select(driver.find_element(By.ID, "id_timeclose_day"))
            day_select.select_by_value(str(dt.day))
            month_select = Select(driver.find_element(By.ID, "id_timeclose_month"))
            month_select.select_by_value(str(dt.month))
            year_select = Select(driver.find_element(By.ID, "id_timeclose_year"))
            year_select.select_by_value(str(dt.year))
            hour_select = Select(driver.find_element(By.ID, "id_timeclose_hour"))
            hour_select.select_by_value(str(dt.hour))
            minute_select = Select(driver.find_element(By.ID, "id_timeclose_minute"))
            minute_select.select_by_value(str(dt.minute))

        
        if row["time_limit"] == 0 or str(row["time_limit"]).strip() == "":
            print("")
        else:
            import re
            seconds = parse_timelimite(row["time_limit"])
            match = re.match(r"(\d+)\s*(\w+)", str(row["time_limit"]).strip())
            value = int(match.group(1)) if match else seconds
            unit = match.group(2).lower() if match else "seconds"
            unit_map = {
                "weeks": "604800",
                "week": "604800",
                "days": "86400",
                "day": "86400",
                "hours": "3600",
                "hour": "3600",
                "minutes": "60",
                "minute": "60",
                "seconds": "1",
                "second": "1"
            }
            id_timelimit_enabled = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "id_timelimit_enabled"))
            )
            if not id_timelimit_enabled.is_selected():
                id_timelimit_enabled.click()
            time_input = driver.find_element(By.ID, "id_timelimit_number")
            time_input.clear()
            time_input.send_keys(str(value))
            timeunit_select = Select(driver.find_element(By.ID, "id_timelimit_timeunit"))
            unit_value = unit_map.get(unit, "1")
            timeunit_select.select_by_value(unit_value)
            # print(f"⏱️ Đã nhập giới hạn thời gian: {value} {unit}")
        if "grade_pass" in row and str(row["grade_pass"]).lower() != "nan":
            grade_pass_value = str(row["grade_pass"]).replace(",", ".")
            grade_pass = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "id_gradepass"))
            )
            grade_pass.clear()
            grade_pass.send_keys(grade_pass_value)

        if "grade_method" in row and str(row["grade_method"]).lower() != "nan":
            try:
                questions_per_page_select = Select(driver.find_element(By.ID, "id_grademethod"))
                questions_per_page_value = str(int(row["grade_method"]))
                questions_per_page_select.select_by_value(questions_per_page_value)
                # print(f"✅ Đã chọn số câu hỏi mỗi trang: {questions_per_page_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn số câu hỏi mỗi trang: {e}")

        # Chọn số câu hỏi mỗi trang nếu có trường trong file Excel
        if "questions_per_page" in row and str(row["questions_per_page"]).lower() != "nan":
            try:
                questions_per_page_select = Select(driver.find_element(By.ID, "id_questionsperpage"))
                questions_per_page_value = str(int(row["questions_per_page"]))
                questions_per_page_select.select_by_value(questions_per_page_value)
                # print(f"✅ Đã chọn số câu hỏi mỗi trang: {questions_per_page_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn số câu hỏi mỗi trang: {e}")

        if "shuffle_questions" in row and str(row["shuffle_questions"]).lower() != "nan":
            try:
                shuffle_questions_select = Select(driver.find_element(By.ID, "id_shuffleanswers"))
                shuffle_questions_value = str(int(row["shuffle_questions"]))
                shuffle_questions_select.select_by_value(shuffle_questions_value)
                # print(f"✅ Đã chọn shuffle_questions: {shuffle_questions_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn shuffle_questions: {e}")


        if "showuserpicture" in row and str(row["showuserpicture"]).lower() != "nan":
            try:
                showuserpicture_select = Select(driver.find_element(By.ID, "id_showuserpicture"))
                showuserpicture_value = str(int(row["showuserpicture"]))
                showuserpicture_select.select_by_value(showuserpicture_value)
                # print(f"✅ Đã chọn showuserpicture: {showuserpicture_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn showuserpicture: {e}")


        if "decimalpoints" in row and str(row["decimalpoints"]).lower() != "nan":
            try:
                decimalpoints_select = Select(driver.find_element(By.ID, "id_decimalpoints"))
                decimalpoints_value = str(int(row["decimalpoints"]))
                decimalpoints_select.select_by_value(decimalpoints_value)
                # print(f"✅ Đã chọn số chữ số thập phân: {decimalpoints_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn số chữ số thập phân: {e}")

        if "questiondecimalpoints" in row and str(row["questiondecimalpoints"]).lower() != "nan":
            try:
                questiondecimalpoints_select = Select(driver.find_element(By.ID, "id_questiondecimalpoints"))
                questiondecimalpoints_value = str(int(row["questiondecimalpoints"]))
                questiondecimalpoints_select.select_by_value(questiondecimalpoints_value)
                # print(f"✅ Đã chọn số chữ số thập phân cho từng câu hỏi: {questiondecimalpoints_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn số chữ số thập phân cho từng câu hỏi: {e}")

        if "seb_requiresafeexambrowser" in row and str(row["seb_requiresafeexambrowser"]).lower() != "nan":
            try:
                seb_select = Select(driver.find_element(By.ID, "id_seb_requiresafeexambrowser"))
                seb_value = str(int(row["seb_requiresafeexambrowser"]))
                seb_select.select_by_value(seb_value)
                # print(f"✅ Đã chọn chế độ Safe Exam Browser: {seb_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn chế độ Safe Exam Browser: {e}")

        if "visible" in row and str(row["visible"]).lower() != "nan":
            try:
                visible_select = Select(driver.find_element(By.ID, "id_visible"))
                visible_value = str(int(row["visible"]))
                visible_select.select_by_value(visible_value)
                # print(f"✅ Đã chọn trạng thái hiển thị: {visible_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn trạng thái hiển thị: {e}")

        if "completion" in row and str(row["completion"]).lower() != "nan":
            try:
                completion_select = Select(driver.find_element(By.ID, "id_completion"))
                completion_value = str(int(row["completion"]))
                completion_select.select_by_value(completion_value)
                # print(f"✅ Đã chọn trạng thái hoàn thành hoạt động: {completion_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn trạng thái hoàn thành hoạt động: {e}")

        if "competency_rule" in row and str(row["competency_rule"]).lower() != "nan":
            try:
                competency_rule_select = Select(driver.find_element(By.ID, "id_competency_rule"))
                competency_rule_value = str(int(row["competency_rule"]))
                competency_rule_select.select_by_value(competency_rule_value)
                # print(f"✅ Đã chọn quy tắc năng lực: {competency_rule_value}")
            except Exception as e:
                print(f"⚠️ Không thể chọn quy tắc năng lực: {e}")
        contest_password = row["contest_password"] if "contest_password" in row and str(row["contest_password"]).lower() != "nan" else None
        if contest_password:
            driver.execute_script(f"document.getElementById('id_progcontestpassword').value='{contest_password}'")
        save_display_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.NAME, "submitbutton"))
        )
        save_display_button.click()

        # Kiểm tra lỗi thiếu tên contest bằng text lấy từ cột expected_result


        if str(row["expected_result"]).lower() == "successful":
            try:
                contest_title = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                    EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{row['contest_name']}')]"))
                )
                if contest_title:
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
        print(f"❌ Lỗi ở dòng {idx+2}: {e}")
        fail_count += 1
        try:
            driver.quit()
        except:
            pass
        return


# Chạy tối đa 5 threads mỗi lần, bỏ qua hàng số 2 trong file Excel
batch_size = 5
total = len(df)
print(total)
for start in range(0, total, batch_size):
    threads = []
    for idx in range(start, min(start + batch_size, total)):
        if idx == 0:  # Bỏ qua hàng số 2 (chỉ số 1)
            continue
        row = df.iloc[idx]
        # Bỏ qua dòng trống cuối file (nếu tất cả giá trị đều rỗng hoặc NaN)
        if row.isnull().all() or all(str(row[col]).strip() == '' or str(row[col]).lower() == 'nan' for col in df.columns):
            continue
        t = threading.Thread(target=run_contest, args=(row, idx))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

input("🔎 Press Enter to close the browser...")

print(f"Tổng số test case thành công: {success_count}")
print(f"Tổng số test case thất bại: {fail_count}")
driver.quit()


