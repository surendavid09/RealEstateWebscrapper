
import requests
from bs4 import BeautifulSoup

"""
Web scrapper that will extract date from a real estate website to include multiple feilds
for all listings with Rock Springs, WY.
"""

l=[]
base_url="http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content

soup=BeautifulSoup(c, "html.parser")

page_nr = soup.find_all("a", {"class": "Page"})[-1].text
print(page_nr)

for page in range(0,int(page_nr)*10,10):
    r = requests.get(base_url+str(page)+".html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c=r.content #loadrequest content into another variable

    soup=BeautifulSoup(c,"html.parser")#pass content through beautifulsoup class

    propertyRow=soup.find_all("div", {"class":"propertyRow"})

    for item in propertyRow:
        d={}
        d["Address"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text
        try:
            d["Locality"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"]=None

        try:
            d["Area"]=item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"]=None
        try:
            d["Bedrooms"]=item.find("span", {"class":"infoBed"}).find("b").text
        except:
            d["Bedrooms"]=None

        try:
            d["Full baths"]=item.find("span", {"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full baths"]=None

        try:
            d["Half baths"]=item.find("span", {"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half baths"]=None
        #using zip function to look at feature name compared to result
        #if feature name is not present - it will move to next set of elements
        for column_group in item.find_all("div", {"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",
            {"class":"featureGroup"}),column_group.find_all("span", {"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text
        d["Price"]=item.find("h4", {"class": "propPrice"}).text.replace("\n","").replace(" ","")
        l.append(d)

#bs4 result set can have findAll method used on each element of set
#need to store values in dictionary - shouldnt use data frame object in iteration

import pandas
df=pandas.DataFrame(l)
df.to_csv("Output.csv")
