from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the class search page
driver.get("https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr=355&honors=F&keywords=83573&promod=F&searchType=all&subject=CSE&term=2247")

# Wait for the page to load completely
driver.implicitly_wait(10)

# Find all elements that display open seats information
# This CSS selector might need to be updated based on the actual page structure
open_seats_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='class-results-cell seats']")


for seat in open_seats_elements:
    print(seat.text)

driver.quit()
