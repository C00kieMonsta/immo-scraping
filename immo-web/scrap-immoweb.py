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

def extractAndAppend(soup):
    # #########################################
    #       1# Extract Info
    # #########################################
    items = soup.findAll("div", {"class": "result-xl"})

    # #########################################
    #       2# Feed CSV with first page
    # #########################################
    with open('csv/immoweb.csv', 'a', newline='', encoding="utf-8") as csvfile:

        filewriter = csv.writer(csvfile)

        for item in items:
            id = item.attrs['id']
            a_tag = item.find('a')
            url = a_tag.attrs['href']
            donnees = a_tag.find("div", {"class": "xl-donnees-bien"})
            price = re.sub('\\s\\s+', ' ', donnees.find("div", {"class": ["xl-price", "rangePrice"]}).text)
            size = re.sub('\\s\\s+', ' ', donnees.find("div", {"class": ["xl-surface-ch"]}).text)
            desc = re.sub('\\s\\s+', ' ', donnees.find("div", {"class": ["xl-desc"]}).text)
            title = re.sub('\\s\\s+', ' ', a_tag.find("div", {"class": "title-bar-left"}).text)
            location = re.sub('\\s\\s+', ' ', a_tag.find("div", {"class": "title-bar-right"}).text)

            if a_tag.find("div", {"class": "xl-photo-bien owl-carousel"}):
                photo = a_tag.find("div", {"class": "xl-photo-bien owl-carousel"}).find("img").attrs['data-src']
            else:
                photo = ''

            # write to csv
            filewriter.writerow([id, url, price, size, title, desc, location, photo])

with open('csv/immoweb.csv', 'w') as csvfile:
    
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|')
    filewriter.writerow(['Id', 'Url', 'Price', 'Size', 'Title', 'Description', 'Location', 'Photo'])

codes_communes_bxl = [1000, 1030, 1040, 1050, 1060, 1070, 1080, 1081, 1082, 1083, 1090, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210]

for code in codes_communes_bxl:

    # #########################################
    #       1# Request page for url
    # #########################################
    url = "https://www.immoweb.be/fr/recherche/maison/a-vendre/bruxelles/" + str(code)
    result = requests.get(url)
    src = result.content

    # #########################################
    #       2# Soup Object
    # #########################################
    print("log info -- extract for commune", str(code), "page 1")
    soup = BeautifulSoup(src, "lxml")

    # #########################################
    #       3# Extract Info
    # #########################################
    numbers = soup.select_one("ul.nav-nummer")
    extractAndAppend(soup)

    # #########################################
    #       4# Feed CSV with additional pages
    # #########################################    
    if numbers:
        number_of_pages = list(map(lambda y: y.text, filter(lambda x: x.find("a"), numbers.findAll("li"))))

        for page_num in number_of_pages:
            print("log info -- extract for commune", str(code), "page", page_num)
            requests.get(url + "?page=" + page_num)
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            extractAndAppend(soup)