import csv
import requests
import re
from bs4 import BeautifulSoup

class Asset:
    def __init__(self, id, url, desc, title, location, photos):
        self.id = id
        self.url = url
        self.desc = desc
        self.title = title
        self.location = location
        self.photos = photos

# make request to desired website
# <div id="results" ...
#   <div id="id_of_item"
#       <a title="small_descriptio" href="link_to_asset"
result = requests.get("https://www.immoweb.be/fr/recherche/maison/a-vendre/bruxelles/1000")

# storing content of request
src = result.content

# BS Object
soup = BeautifulSoup(src, "lxml")
results = soup.find(id='result')
items = soup.findAll("div", {"class": "result-xl"})

# list of assets
assets = []


with open('csv/immoweb.csv', 'w') as csvfile:
    
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['ID', 'Url', 'Description', 'Title', 'Location'])

    for item in items:
        id = item.attrs['id']
        a_tag = item.find('a')
        url = a_tag.attrs['href']
        desc = a_tag.attrs['title']
        title = re.sub('\s\s+', ' ', a_tag.find("div", {"class": "title-bar-left"}).text)
        location = re.sub('\s\s+', ' ', a_tag.find("div", {"class": "title-bar-right"}).text)
        photos = map(lambda x: x.attrs['data-src'] , a_tag.find("div", {"class": "xl-photo-bien owl-carousel"}).findAll("img"))
        
        # write to csv
        filewriter.writerow([id, url, title, location])

        # asset = Asset(id, url, desc, title, location, list(photos))
        # assets.append(asset)