from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup Chrome options for headless mode
options = Options()
options.add_argument("--headless")  # Ensure headless mode is activated

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to check for open seats
def check_for_open_seats():
    while True:
        # Navigate to the class search page
        driver.get("https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr=355&honors=F&keywords=83573&promod=F&searchType=all&subject=CSE&term=2247")
        
        # Wait for the page to load completely
        driver.implicitly_wait(10)
        
        # Find all elements that display open seats information
        open_seats_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='class-results-cell seats']")
        
        for seat in open_seats_elements:
            # Extract the text and split it to check the number of open seats
            seats_info = seat.text.split(" of ")
            if len(seats_info) == 2 and int(seats_info[0]) > 0:
                print(f"Open seats available: {seats_info[0]}")
                return  # Exit the function if open seats are found
            else:
                print("No open seats, reloading...")
                time.sleep(5)  # Wait for 5 seconds before reloading the page

# Run the check
check_for_open_seats()

# Close the driver after checking
driver.quit()