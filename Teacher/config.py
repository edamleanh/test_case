# Configuration file for test settings

# ChromeDriver path
CHROME_DRIVER_PATH = r"C:\Users\edaml\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"

# Application URLs
# BASE_URL = "http://172.29.64.156/moodle311"
BASE_URL = "http://172.29.64.156/moodletest311/moodle"
LOGIN_URL = f"{BASE_URL}/login"
MOODLE_URL = BASE_URL

# Test credentials
USERNAME = "admin"
PASSWORD = "C@pstone2025"

# Multiple test accounts for parallel testing
TEST_ACCOUNTS = [
    {"username": "admin", "password": "C@pstone2025"},
    {"username": "admin", "password": "C@pstone2025"},
    {"username": "admin", "password": "C@pstone2025"},
    {"username": "admin", "password": "C@pstone2025"},
    {"username": "admin", "password": "C@pstone2025"},
]

# Timeout settings
DEFAULT_TIMEOUT = 10

ID_PROBLEMS = "que143"
# {
#     {"username": "teacher2", "password": "C@pstone2025"},
#     {"username": "teacher3", "password": "C@pstone2025"},
#     {"username": "teacher4", "password": "C@pstone2025"},
#     {"username": "teacher5", "password": "C@pstone2025"},
#     {"username": "teacher6", "password": "C@pstone2025"},
#     {"username": "teacher7", "password": "C@pstone2025"},
#     {"username": "teacher8", "password": "C@pstone2025"},
#     {"username": "teacher9", "password": "C@pstone2025"},
#     {"username": "teacher10", "password": "C@pstone2025"}
# }

TEST_QUESTION=[
    {
        "name": "question1",  
        "description": "Description test",  
        "file_path": r"C:\Users\edaml\Downloads\test_data_1.zip",  
        "type_id": 1, 
        "language_id": 8  
    },
    {
        "name": "question2",  
        "description": "Description test",  
        "file_path": r"C:\Users\edaml\Downloads\test_data_1.zip",  
        "type_id": 1, 
        "language_id": 8  
    },
    {
        "name": "question3",  
        "description": "Description test",  
        "file_path": r"C:\Users\edaml\Downloads\test_data_1.zip",  
        "type_id": 1, 
        "language_id": 8  
    },
    {
        "name": "question4",  
        "description": "Description test",  
        "file_path": r"C:\Users\edaml\Downloads\test_data_1.zip",  
        "type_id": 1, 
        "language_id": 8  
    },
    {
        "name": "question5",  
        "description": "Description test",  
        "file_path": r"C:\Users\edaml\Downloads\test_data_1.zip",  
        "type_id": 1, 
        "language_id": 8  
    }
]
