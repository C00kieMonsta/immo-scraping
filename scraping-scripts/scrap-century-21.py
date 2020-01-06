import csv
import requests
import re
import json
from bs4 import BeautifulSoup

# #########################################
#       1# Request page for url
# #########################################
url = "https://api.century21.be/api/v1/properties/advancedsearch"
payload = {"epcMinRange":0,"start":0,"nbResults":30000,"orderBy":"updatedAt","score":{},"reference":"null","propertyType":["HOUSE"],"transferType":["SALE"],"onlyNew":"null","minPrice":0,"countryCode":["BE"]}
result = requests.post(url, data=json.dumps(payload))
src = result.content
print(src)