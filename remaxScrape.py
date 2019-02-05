from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1920,1080")
chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(executable_path=os.path.abspath(r"C:\Users\Nic\Documents\chromedriver.exe"),   chrome_options=chrome_options)
driver.get("https://www.remax.ca/on/kingston-real-estate?page=1")
#time.sleep(10)
myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'homePage-button-view')))

listButton = driver.find_element_by_id('homePage-button-view')
listButton.click()
time.sleep(2)

html = BeautifulSoup(driver.page_source, 'html.parser')

abbToFull = {'ST': 'street', 'St': 'street', 'STREET': 'street', 'ROAD': 'road', 'RD': 'road', 'Rd': 'road',
             'DR': 'drive', 'DRIVE': 'drive', 'CT': 'court', 'COURT': 'court', 'WAY': 'way', 'CRES': 'crescent',
             'Cres': 'crescent', 'LN': 'lane', 'Lane': 'lane', 'PL': 'place', 'AVE': 'avenue', 'Pl': 'place',
             'AVENUE': 'avenue', 'TRL': 'trail', 'TER': 'terrace', 'CIR': 'circle', 'BLVD': 'boulevard'}

df = pd.DataFrame(columns=['price', 'number', 'street_name', 'street_type', 'city', 'province'])

filename = "listings.csv"
f = open(filename, "w")
headers = "price, number, streetName, streetType, city, province\n"
f.write(headers)

i = 2
#while EC.presence_of_element_located((By.XPATH, "//a[@translate='gallery.next']")):
while i < 25:    
    html = BeautifulSoup(driver.page_source, 'html.parser')

    
    mydivs = html.findAll("div", {"class": "left-content flex-one"})

    for div in mydivs:
        price = div.findChildren("h3", recursive=False)[0].text
        price = price.replace("$", "")
        price = price.replace(",", "")
        price = price.strip()
        
        addressInfo = div.findChildren("app-listing-address", recursive=True)[0].findChildren('span', recursive=False)
        number = re.match('^(.*?)[a-zA-Z]', addressInfo[0].text)[0][:-2]
        if number:
            number = re.match('[0-9]+', number)[0]
        streetStart = re.search('^(.*?)[a-zA-Z]', addressInfo[0].text).end()
        # Start substring after the number of the street ends, and end at -1 to remove the comma
        street = addressInfo[0].text[streetStart-1:-2]
        street = street.split(" ")
        street_type = street.pop(-1)
        if street_type in abbToFull:
            street_type = abbToFull[street_type]
        street_name = ''.join(map(str, street))
        city = addressInfo[1].text[:-2]
        province = addressInfo[2].text[:-2]
        postal = addressInfo[3].text
        if city == "Kingston" or city == "kingston":
            f.write(price + "," + number + "," + street_name + "," + street_type + "," + city + "," + province + "\n")
            
    
    
    driver.get("https://www.remax.ca/on/kingston-real-estate?page=" + str(i))
    time.sleep(5)
    i += 1

f.close()