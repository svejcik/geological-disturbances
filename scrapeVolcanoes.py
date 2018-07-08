import pandas as pd
import re
import sys
from urllib import request
from bs4 import BeautifulSoup
def is_volcano_entry(table_row):
    cells = table_row.findAll("td")
    if len(cells) > 5:
        return True
    else:
        return False
def get_all_volcanoes(html_soup):
    volcanoes = []
    all_rows_in_html_page = html_soup.findAll("tr")
    #sys.stderr.write(repr(html_soup)+'\n')
    for table_row in all_rows_in_html_page:
        if is_volcano_entry(table_row):
            row_cells = table_row.findAll("td")
            volcano_entry = {
                "name":row_cells[0].text.strip(),
                "country":row_cells[1].text.strip(),
                "type":row_cells[2].text.strip(),
                "latitude":row_cells[3].text.strip(),
                "longitude":row_cells[4].text.strip(),
                "elevation":row_cells[5].text.strip()
                }
            volcanoes.append(volcano_entry)
    return volcanoes
if __name__=='__main__':
    html = request.urlopen("http://volcano.oregonstate.edu/volcano_table")
    html_soup = BeautifulSoup(html, 'html.parser')
    volcano_list = get_all_volcanoes(html_soup)    
    indf = pd.DataFrame(volcano_list)
    sys.stderr.write(repr(indf.head()) +'\n')
    df = indf.convert_objects(convert_numeric=True)
    # This says if latitude > 0 then set country = 'Northern'
    df.loc[df.latitude > 0, 'Hemisphere'] = 'Northern'
    df.loc[df.latitude < 0, 'Hemisphere'] = 'Southern'
    # This says if longitude < 0 then set longitude = -1
    df.loc[df.longitude < 0, 'EW Hemisphere'] = 'Western'
    df.loc[df.longitude > 0, 'EW Hemisphere'] = 'Eastern'
    # Japanese Volcanoes
    df.loc[df.country=='Japan',['latitude','longitude']]
    # if I had followed up the above with an assignment like ...=0 then it would have given lat and long of 0 to all japanese volcanoes.
    #
    # This returns the dataframe sorted by how close to the greenwich meridian.
    df.loc[(df.longitude-0.).abs().argsort()]
    print(df.head(10))
    df.to_csv('MyVolcanoes.csv')
    
    
