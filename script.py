import requests
import json

#Fall2024- 2247- check browser URL for this val
TERM_VAL = '2247'

#first three chars of the class (SUBJECT = CSE to track CSE450)
SUBJECT = 'CSE'

#last three chars of the class (CLASS_NUM = 450 to track CSE450)
CLASS_NUM = '450'


# Class Search URL
url = f"https://eadvs-cscc-catalog-api.apps.asu.edu/catalog-microservices/api/v1/search/classes?&refine=Y&campusOrOnlineSelection=A&catalogNbr={CLASS_NUM}&honors=F&promod=F&searchType=all&subject={SUBJECT}&term={TERM_VAL}"

# Authorization header
headers = {
    'Authorization': 'Bearer null'
}

while True:
    # Make the GET request with NULL auth
    response = requests.get(url, headers=headers)

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
            
            # send req again if no spots are available
            if (enrlcap == totenrl) :
                print("No Spots Available-- trying again...")
                continue
            else : # enroll and exit
                openspots = enrlcap - totenrl
                print(openspots, " spots available!")
                exit(0)  
    else:
        print("No class information found.")
        exit(1)
        
