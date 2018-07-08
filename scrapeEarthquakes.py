import pandas as pd
import re
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
def get_all_earthquakes(html_soup):
    earthquakes = html_soup.findAll("li",attrs={'class':'eqitem'})
    earthquakedata = []
    #sys.stderr.write(repr(html_soup)+'\n')
    for earthquake in earthquakes:
        title = earthquake.find(attrs={'class':'title'})
        data = earthquake.findAll('span')
        row_cells = earthquake.findAll("span")
        earthquake_entry = {
            "name":title.text,
            "usgsref":title['href'],
            "strength":row_cells[0].text.strip(),
            "datetime":row_cells[1].text.strip(),
            "depthKM":row_cells[2].text.strip().split()[0]
        }
        earthquakedata.append(earthquake_entry)
    return earthquakedata

def getEarthquakeDetails(soup):
    details = {}
    # the usgs page has a *lot* more data than what I'm grabbing now.
    evheader = soup.find('header',attrs={'class':'event-header'})
    location = evheader.find('span',attrs={'class':'event-coordinates'})
    details['location'] = location.text
    return details

if __name__=='__main__':
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://earthquake.usgs.gov/earthquakes/browse/m6-world.php?year=2001')
    html = browser.page_source
    html_soup = BeautifulSoup(html, 'html.parser')
    earthquake_list = get_all_earthquakes(html_soup)
    earthquakedf = pd.DataFrame(earthquake_list)
    # This part is really slow. Probably more sense to use the fdsnws
    # catalog with a dedicated api (https://earthquake.usgs.gov/fdsnws/).
    for earthquake in earthquake_list:
        browser.get(earthquake['usgsref'])
        detailSoup = BeautifulSoup(browser.page_source, 'html.parser')
        earthquake.update(getEarthquakeDetails(detailSoup))
    earthquakedf = pd.DataFrame(earthquake_list)
    sys.stderr.write(repr(earthquakedf.head(5)) +'\n')
    
    
