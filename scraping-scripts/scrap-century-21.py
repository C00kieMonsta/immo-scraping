import csv
import requests
import re
import json
from bs4 import BeautifulSoup


def extractAndAppend(properties):

    # #########################################
    #       2# Feed CSV with first page
    # #########################################
    with open('csv/century_21.csv', 'a', newline='', encoding="utf-8") as csvfile:

        filewriter = csv.writer(csvfile)

        for item in properties:
            id = item['id']
            url = 'https://www.century21.be/nl/onze-vastgoed/details/' + item['id']
            price = item['price'] if hasattr(item, 'price') else ''
            size = 1 # lots of different things
            title = ''
            desc = item['descriptionFR'] if hasattr(item, 'descriptionFR') else (item['descriptionNL'] if hasattr(item, 'descriptionNL') else '')
            location = item['address']['cityName'] + item['address']['postalCode']
            photo = photo_url + item['medias'][0]['id'] if hasattr(item, 'medias') else ''
            
            

            # write to csv
            filewriter.writerow([id, url, price, size, title, desc, location, photo])

# #########################################
#       1# Request page for url
# #########################################
url = 'https://api.century21.be/api/v1/properties/advancedsearch'
photo_url = 'https://static.century21.be/images/720'
payload = '{"epcMinRange":0,"start":0,"nbResults":300000,"orderBy":"updatedAt","score":{},"reference":null,"propertyType":["HOUSE"],"transferType":["SALE"],"onlyNew":null,"minPrice":0,"countryCode":["BE"]}'

# #########################################
#       2# Extract data and make json
# #########################################
result = requests.post(url, json=json.loads(payload))
src = result.content
properties = json.loads(src)['properties']

# #########################################
#       3# Create csv file
# #########################################
print("There are", len(properties), "properties")
extractAndAppend(properties)