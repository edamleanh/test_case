import threading
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_DRIVER_PATH, BASE_URL, TEST_ACCOUNTS, DEFAULT_TIMEOUT

def login_test(account_index, username, password):
    """
    Hàm test login cho một tài khoản
    """
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
            
            # Keep browser open for a while to see result
            time.sleep(10)
            
        except Exception as login_error:
            print(f"❌ Thread {account_index + 1}: LOGIN FAILED for {username} - {login_error}")
            
    except Exception as e:
        print(f"💥 Thread {account_index + 1}: ERROR for {username} - {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
                print(f"🔒 Thread {account_index + 1}: Browser closed for {username}")
            except:
                pass

def run_parallel_login_tests():
    """
    Chạy test login song song cho 10 tài khoản
    """
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
        
        # Delay nhỏ giữa các thread để tránh quá tải
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
