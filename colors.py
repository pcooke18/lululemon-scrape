from bs4 import BeautifulSoup
import requests, re

url = "https://shop.lululemon.com/p/men-pants/Relaxed-Tapered-Trouser/_/prod11250229?color=27597"
myResponse = requests.get(url)

if myResponse.status_code == 200:

    soup = BeautifulSoup(myResponse.content, "html.parser")

    # Get product information (name and URL to specific product page)
    #colors = soup.find_all('a', class_ = 'link lll-font-weight-medium')
    product_color = soup.find(class_ = "buttonTileGroupWrapper-2PyXd").find_all("div")
    
    colors = []
    colors_str = ""

    [colors.append(x.get("aria-label")) for x in product_color]
    
    colors_str = ', '.join([color for idx, color in enumerate(sorted(colors)) if idx < len(colors) - 1]) + ' and ' + sorted(colors)[-1]
    print(colors_str)