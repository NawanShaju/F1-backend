import requests
from bs4 import BeautifulSoup

def scrap_driver_stats(driver_first: str, driver_last: str):
    driver_first = driver_first.lower().strip()
    driver_last = driver_last.lower().strip()
        
    url = f"https://www.formula1.com/en/drivers/{driver_first}-{driver_last}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    infos = soup.find_all("div", {"class", "DataGrid-module_item__cs9Zd"})
    
    stats_info = {}
    for info in infos:
        catogery = info.find("dt", {"class", "DataGrid-module_title__hXN-n typography-module_body-xs-semibold__Fyfwn"}).get_text(strip=True)
        result = info.find("dd", {"class", "DataGrid-module_description__e-Mnw typography-module_display-l-bold__m1yaJ typography-module_lg_display-xl-bold__4nIv1"}).get_text(strip=True)
        
        stats_info[catogery] = result
    
    return stats_info