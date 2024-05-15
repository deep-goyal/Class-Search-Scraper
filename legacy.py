from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time

#consts
USERNAME = "dgoyal15"


#instantiate driver
driver = webdriver.Chrome()

#open the myasu url
driver.get("https://weblogin.asu.edu/cas/login?service=https%3A%2F%2Fweblogin.asu.edu%2Fcgi-bin%2Fcas-login%3Fcallapp%3Dhttps%253A%252F%252Fwebapp4.asu.edu%252Fmyasu%252F%253Finit%253Dfalse")



unamefield = driver.find_element(By.ID, "username")

passfield = driver.find_element(By.ID, "password")

unamefield.send_keys(USERNAME)
passfield.send_keys(PASSWORD)

submitbtn = driver.find_element(By.NAME, "submit")

submitbtn.click()

time.sleep(15)

