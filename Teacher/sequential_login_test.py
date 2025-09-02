from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_DRIVER_PATH, BASE_URL, TEST_ACCOUNTS, DEFAULT_TIMEOUT
import time

def test_single_account(username, password, account_number):
    """
    Test login cho một tài khoản
    """
    driver = None
    try:
        print(f"\n🚀 Testing account {account_number}: {username}")
        print("-" * 40)
        
        # Setup WebDriver
        service = EdgeService(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        
        # Open Moodle site
        driver.get(BASE_URL)
        
        # Click login link
        login_button = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
        )
        login_button.click()
        
        # Enter credentials
        username_input = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        
        username_input.send_keys(username)
        password_input.send_keys(password + Keys.RETURN)
        
        # Check if login successful
        try:
            WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Dashboard"))
            )
            print(f"✅ Account {account_number} ({username}): LOGIN SUCCESSFUL")
            
            # Keep browser open for 3 seconds
            time.sleep(3)
            return True
            
        except Exception:
            print(f"❌ Account {account_number} ({username}): LOGIN FAILED")
            time.sleep(2)
            return False
            
    except Exception as e:
        print(f"💥 Account {account_number} ({username}): ERROR - {e}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def run_sequential_login_tests():
    """
    Chạy test login tuần tự cho 10 tài khoản
    """
    print("🚀 Starting sequential login tests for 10 accounts...")
    print("=" * 50)
    
    successful_logins = 0
    failed_logins = 0
    
    for i, account in enumerate(TEST_ACCOUNTS, 1):
        username = account["username"]
        password = account["password"]
        
        success = test_single_account(username, password, i)
        
        if success:
            successful_logins += 1
        else:
            failed_logins += 1
        
        # Small delay between tests
        if i < len(TEST_ACCOUNTS):
            print("⏳ Waiting 2 seconds before next test...")
            time.sleep(2)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"✅ Successful logins: {successful_logins}")
    print(f"❌ Failed logins: {failed_logins}")
    print(f"📈 Success rate: {(successful_logins/len(TEST_ACCOUNTS)*100):.1f}%")
    print("=" * 50)

if __name__ == "__main__":
    run_sequential_login_tests()
