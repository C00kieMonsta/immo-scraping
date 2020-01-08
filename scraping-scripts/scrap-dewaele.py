import csv
import requests
import re
import json
import base64

def extractAndAppend(properties):

    # #########################################
    #       2# Feed CSV with first page
    # #########################################
    with open('csv/dewaele.csv', 'a', newline='', encoding="utf-8") as csvfile:

        filewriter = csv.writer(csvfile)

        for item in properties:
            id = item['id']
            url = 'https://www.dewaele.com/en/for-sale/' + item['a_postcode'] + '-' + item['a_gemeente'] + '/no-type/' + item['a_ref']
            price = item['sort_price'] if hasattr(item, 'sort_price') else ''
            size = item['b_woonopp']
            title = item['a_titel']
            desc = item['a_beschrkort']
            location = item['a_postcode'] + item['a_gemeente'] + item['a_straat']
            photo = item['picture_url'] if hasattr(item, 'picture_url') else ''
        
            # write to csv
            filewriter.writerow([id, url, price, size, title, desc, location, photo])

# #########################################
#       1# Request page for url
# #########################################

properties = []

for i in range(1, 113):
    params = '&filter[region]=&filter[region_long]=0&filter[region_lat]=0&filter[status_type]=2&filter[postal]=&filter[city]=&filter[parent_city]=&filter[parent_label]=&filter[f_c]=&filter[language]=en&filter[e_id]=46484&filter[dir]=desc&filter[order]=is_new&filter[min_price]=0&filter[max_price]=0&filter[min_rent_price]=&filter[max_rent_price]=&filter[bdrms]=0&filter[type]=&filter[b_id]=&filter[min_bw_opp]=0&filter[max_bw_opp]=0&filter[min_g_opp]=0&filter[max_g_opp]=0&filter[keywords]=&page=' + str(i)

    # Standard Base64 Encoding
    encodedBytes = base64.b64encode(params.encode("utf-8"))
    base64params = str(encodedBytes, "utf-8")

    url = 'https://www.dewaele.com/?ACT=108&cache=off&hash=' + base64params

    # #########################################
    #       2# Extract data and make json
    # #########################################
    result = requests.get(url)
    src = result.content
    properties = properties + json.loads(src)['properties']

# #########################################
#       3# Create csv file
# #########################################
print("There are", len(properties), "properties")
extractAndAppend(properties)