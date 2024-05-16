import requests
import json
import discord
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# PING CONSTANTS
TOKEN = ''                              # Bot token -- DO NOT FORGET TO REDACT IT BEFORE SHARING
CHANNEL_ID = '1240355389309059072'      # Channel ID

# CLASS INFO CONSTANTS
TERM_VAL = '2247'                       # Fall2024- 2247- check browser URL for this val
SUBJECT = 'CSE'                         # first three chars of the class (SUBJECT = CSE to track CSE450)
CLASS_NUM = '475'                       # last three chars of the class (CLASS_NUM = 450 to track CSE450)

# webpage url (for webpage search)
WEBPAGE_URL = f"https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&catalogNbr={CLASS_NUM}&honors=F&promod=F&searchType=all&subject={SUBJECT}&term={TERM_VAL}"

def ping_user(openspots):
    """
    This function sends a message to a channel in the discord about the availability of a spot    

    Args:
        openspots (int): number of open spots
        
    """
    # Initialize the discord client
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        channel = client.get_channel(int(CHANNEL_ID))
        await channel.send("@everyone")
        await channel.send("@everyone")
        await channel.send(f'{openspots} spots open in {SUBJECT} {CLASS_NUM}')
        await channel.send("@everyone")
        await channel.send("@everyone")
        await client.close()
        
    client.run(TOKEN)
    return

def api_search():
    """
    This function sends a request to the asu catalog api to fetch the number of open spots.
    
    NOTE: This search produces accurate results for small classes only.
    """
    # Class Search URL
    endpoint = f"https://eadvs-cscc-catalog-api.apps.asu.edu/catalog-microservices/api/v1/search/classes?&refine=Y&campusOrOnlineSelection=A&catalogNbr={CLASS_NUM}&honors=F&promod=F&searchType=all&subject={SUBJECT}&term={TERM_VAL}"

    # Authorization header
    headers = {
        'Authorization': 'Bearer null'
    }
    
    while True:
        try:
            # Make the GET request with NULL auth
            response = requests.get(endpoint, headers=headers)

            # Parse the JSON response
            data = json.loads(response.text)

            # Extract seat counts
            # JSON Hierarchy: classes[]->seat_info->ENRL_CAP/ENRL_TOT
            if 'classes' in data:
                for class_info in data['classes']:
                    seat_info = class_info.get('seatInfo', {})
                    
                    # class capacity
                    enrlcap = seat_info.get('ENRL_CAP')
                    
                    #total enrollment
                    totenrl = seat_info.get('ENRL_TOT')
                    
                    if (enrlcap > totenrl) :
                        openspots = enrlcap - totenrl
                        ping_user(openspots)
                        return
                    
        except Exception as e:
            print(f"Exception <{e}> occurred")
        
        #delay before next iteration    
        time.sleep(60)
        
def webpage_search():
    """
    This function uses selenium to render an actual headless browser instance and fetch the open spots.
    
    NOTE: This search takes about a min in each iteration, but produces accurate seat count for all classes.
    """
    #setup options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--blink-settings=imagesEnabled=false")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    while True:
        try:
            #load the page
            driver.get(WEBPAGE_URL)
            
            #wait 10 secs for complete render
            driver.implicitly_wait(10)

            #find all open seats elements from dom
            open_seat_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='class-results-cell seats']")
            
            for seat_element in open_seat_elements:
                #extract seat count (format: 0 of XX)
                seats_info = seat_element.text.split(" of ")
                if len(seats_info) == 2 and int(seats_info[0]) > 0:
                    ping_user(seats_info[0])
                    driver.quit()
                    return
                    
        except Exception as e:
            print(f"Exception {e} occurred")
            
        time.sleep(60)
    
if __name__ == "__main__":
    # call api_search for smaller classes (0-80 spots)
    webpage_search()
    api_search()