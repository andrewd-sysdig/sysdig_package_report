# Quickly hacked together on a Friday night, no error handling....
# Make sure to have 2 environment variables set
# export API_TOKEN="<Your Sysdig Secure API Token>""
# export API_ENDPOINT="https://app.au1.sysdig.com"

import requests
import os
import json
import csv

API_TOKEN = os.getenv('API_TOKEN') # Your Sysdig Secure API Token from User Profile
API_ENDPOINT = os.getenv('API_ENDPOINT') # Your Sysdig Secure API Endpoint, ie https://app.au1.sysdig.com

header = {'Authorization': 'Bearer ' + API_TOKEN}

# Get list of image IDs
url = API_ENDPOINT + "/api/scanning/v1/resultsDirect"
response = requests.get(url, headers=header)
imageList = response.json()
#print(jsonResponse["vulns"]);

result_list = []


for images in imageList["results"]:
    url = API_ENDPOINT + "/api/scanning/v1/images/by_id/" + images['imageId'] + "/vulnDirect/non-os"
    response = requests.get(url, headers=header)
    jsonResponse = response.json()
    for data in jsonResponse["vulns"]:
        if data['package_name'] == "log4j": # Filter only if package_name is log4j
            print("log4j Package found in image" + images['fullTag'])
            dict_data = {
                "fullTag": images['fullTag'],
                "imageID": images['imageId'],
                "vuln": data['vuln'],
                "vulnrabilityId": data['vuln'],
                "package": data['package'],
                "packageCPE": data['package_cpe'],
                "packageName": data['package_name'],
                "packagePath": data['package_path'],
                "packageType": data['package_type'],
                "severity": data['severity']
            }
            result_list.append(dict_data)

# Output JSON Results to terminal
print(json.dumps(result_list,indent=4, sort_keys=True))

# Write json file
with open('output.json', 'w') as outfile:
    json.dump(result_list, outfile)

# Write CSV file
csv_columns = ['fullTag','imageID','vuln', 'vulnrabilityId', 'package', 'packageCPE', 'packageName', 'packagePath', 'packageType', 'severity' ]
csv_file = "output.csv"
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in result_list:
        writer.writerow(data)
