from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

start_url="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome('C:\class127\chromedriver_win32\chromedriver.exe')
browser.get(start_url)
time.sleep(15)
planet_data=[]
new_planet_data=[]
final_planet_data=[]
def scrap():
    headers=["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type"
    ,"planet_radius","orbital_radius","orbital_period","eccentricity"]
    

    for i in range(1,448):
        soup=BeautifulSoup(browser.page_source,'html.parser')
        for ul_tag in soup.find_all('ul',attrs={'class','exoplanet'}):
            li_tags=ul_tag.find_all('li')

            temp_list=[]

            for index,li_tag in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tag.find_all('a')[0].contents[0])

                else:
                    try:
                        temp_list.append(li_tag.contents[0])

                    except:
                        temp_list.append(' ')

            hyperlink_li_tag=li_tags[0]
            temp_list.append('https://exoplanets.nasa.gov/'+hyperlink_li_tag.find_all('a',href=True)[0]['href'])

            planet_data.append(temp_list)

        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()

def scrap_more_data(hyperlink):
     try:
         page=requests.get(hyperlink)
         soap=BeautifulSoap(page.content,'html.parsel')
         temp_list=[]

         for tr_tag in soap.find_all('tr',attrs={'class':'fact_row'}):
             td_tags=tr_tag.find_all('td')

             for td_tag in td_tags:
                 try:
                     temp_list.append(td_tag.find_all('div',attrs={'class':'value'})[0].contents[0])
                 except:
                     temp_list.append(" ")

             new_planet_data.append(temp_list)
     except:
         time.sleep(1)
         scrap_more_data(hyperlink)#recursively calling the function

scrap()

for index,data in enumerate(planet_data):
    scrap_more_data(data[5])
    print(f'{index+1} page done')

for index,data in enumerate(planet_data):
    final_planet_data.append(data+final_planet_data[index])
    #new_planet_data_element=new_planet_data[index]



    with open('final.csv','w') as f:
        csv_writer=csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(final_planet_data)

    




    

                
                

            


