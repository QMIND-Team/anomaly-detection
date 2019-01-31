from urllib.request import urlopen as ureq
import requests
from bs4 import BeautifulSoup as Soup

# opens file to write to
filename = "listings.csv"
f = open(filename, "w")
headers = "price, number, streetName, streetType, city, province\n"
f.write(headers)


streetTypeList = ['ST', 'St', 'STREET', 'ROAD', 'RD', 'Rd', 'DR', 'CT', 'COURT', 'WAY', 'CRES', 'Cres', 'LN', 'Lane',
                  'PL', 'AVE', 'Pl', 'AVENUE', 'TRL', 'TER', 'CIR', 'BLVD']

lowerStreetType = ['street', 'avenue', 'road', 'drive', 'court', 'way', 'crescent', 'lane', 'place', 'trail']

abbToFull = {'ST': 'street', 'St': 'street', 'STREET': 'street', 'ROAD': 'road', 'RD': 'road', 'Rd': 'road',
             'DR': 'drive', 'DRIVE': 'drive', 'CT': 'court', 'COURT': 'court', 'WAY': 'way', 'CRES': 'crescent',
             'Cres': 'crescent', 'LN': 'lane', 'Lane': 'lane', 'PL': 'place', 'AVE': 'avenue', 'Pl': 'place',
             'AVENUE': 'avenue', 'TRL': 'trail', 'TER': 'terrace', 'CIR': 'circle', 'BLVD': 'boulevard'}

for x in range(1, 10):
    my_url = 'https://www.point2homes.com/CA/Real-Estate-Listings/ON/Kingston.html?location=Kingston%2C+ON&search_mode=' \
         'location&page={}&SelectedView=listings&LocationGeoId=521492&location_changed=&ajax=1'.format(x)


    def get_page_source(urlIn):
        url = urlIn
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=header)
        return response.text

    # opening connection with page and grabbing the html
    # uClient = ureq(my_url)
    # page_html = uClient.read()
    # uClient.close()

    # parses html
    page_soup = Soup(get_page_source(my_url), "html.parser")

    # grabs each housing listing container
    containers = page_soup.findAll("div", {"class": "item-header-cnt"})

    # iterates through all containers on page and save address and price information
    for container in containers:
        streetbool = True
        # getting price data and cleaning it by removing symbols and whitespace
        price_data = container.findAll("div", {"class": "price"})
        price = price_data[0].text.strip()
        price = price.replace("$", "")
        price = price.replace("CAD", "")
        price = price.replace(",", "")
        price = price.strip()

        # getting address and splitting it into different key attributes
        address = container.div.div["data-address"]
        address, city, province = address.split(",")
        if "Lot" in address:
            del address
            break

        elif len(address.split(" ")) == 3:
            number, streetName, streetType = address.split(" ")
            if "Highway" in streetName:
                streetName = streetName + " " + streetType
                streetType = "Highway"

        elif len(address.split(" ")) == 4:
            number, name1, name2, streetType = address.split(" ")
            streetName = name1 + " " + name2
            if "Highway" in streetName:
                streetName = streetName + " " + streetType
                streetType = "Highway"

        elif len(address.split(" ")) == 5:
            number, name1, name2, name3, streetType = address.split(" ")
            streetName = name1 + " " + name2 + " " + name3
            if "Highway" in streetName:
                streetName = streetName + " " + streetType
                streetType = "highway"
        for word in streetTypeList:
            if streetType == word:
                streetType = abbToFull[word]

        try:
            streetType = int(streetType)
            streetbool = False
        except:
            pass
        if streetbool:
            # f.write(price + "," + number + "," + address + "," + city + "," + province + "\n")
            f.write(price + "," + number + "," + streetName + "," + streetType + "," + city + "," + province + "\n")

f.close()
