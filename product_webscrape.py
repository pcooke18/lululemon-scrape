from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests, re
import time

url = "https://shop.lululemon.com/c/men-pants/_/N-7ub"
myResponse = requests.get(url)

if myResponse.status_code == 200:

    soup = BeautifulSoup(myResponse.content, "html.parser")

    # Get product information (name and URL to specific product page)
    product = soup.find_all('a', class_ = 'link lll-font-weight-medium')

    prod_name = []
    [prod_name.append(x.strings) for x in product]

    url_base = "https://shop.lululemon.com"

    prod_url = []
    [prod_url.append(url_base + x.get('href')) for x in product]

    # Get information about price
    price = soup.find_all("span", class_= "price-1jnQj")

    prod_price = []
    [prod_price.append(x.span.text) for x in price]
    prod_price = [p.lstrip("$") for p in prod_price] #another way to accomplish this: prod_price = [x[1:] for x in prod_price]

## Test out whether I can replicate and use a link from the prod_url to access information on the specific page

design = []
fabric = []

for i in prod_url:

    url2 = i
    myResponse2 = requests.get(url2)
    
    if myResponse2.status_code == 200:
        soup2 = BeautifulSoup(myResponse2.content, "html.parser")
        
        design.append(soup2.find("span", class_ = "accordionItemHeadingTitle-3g5e8").string) #design
        fabric.append(soup2.find_all("span", class_ = "accordionItemHeadingTitle-3g5e8")[1].text.split("(",1)[0]) #materials
    else:
        print("This link is not updatting correctly")
    
    time.sleep(5)

lulu_dict = {
    "Product Name" : prod_name, 
    "Price": prod_price, 
    "Design": design, 
    "Material": fabric, 
    "Link": prod_url
    }

lulu_df = pd.DataFrame(lulu_dict)
print(lulu_df)

lulu_df.to_csv("/Users/piersoncooke/GitHub Practice Repos/lululemon-scrape/first_attempt.csv", index = False)

# colors = []
# temp1 = soup.find_all("img", class_ = "colorSwatchImg-2mYJB")
# [colors.append(x.get("alt")) for x in temp1]
# once I figure out how to select the colors I want to join the list and then paste in as a column value