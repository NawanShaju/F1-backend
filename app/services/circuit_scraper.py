import requests
from bs4 import BeautifulSoup

def scrap_circuit_info(year: str, country: str):
    country = country.lower().replace(' ', '-')
    url = f"https://www.formula1.com/en/racing/{year}/{country}"
    
    response = requests.get(url)
    
    infos = {}
    
    soup = BeautifulSoup(response.content, "html.parser")
    infos['circuit img'] = soup.find("img", {'class': 'w-full h-full object-contain'}).get('src')
    
    key = soup.find("dt", {'class': 'typography-module_body-s-compact-semibold__MeKMi text-text-3'}).get_text(strip=True).lower()
    infos[key] = soup.find("dd", {'class': 'typography-module_desktop-headline-small-bold__4DueK text-text-5 mt-px-4 lg:mt-px-12'}).get_text(strip=True).lower()
    
    keys = soup.find_all("dt", {'class': 'typography-module_body-xs-semibold__Fyfwn text-text-3'})
    values = soup.find_all("dd", {'class': 'typography-module_display-l-bold__m1yaJ text-text-5 mt-px-4 lg:mt-px-12'})
    
    for k, v in zip(keys, values):
        k = k.get_text(strip=True).lower()
        infos[k] = v.get_text(strip=True).lower()
        
    infos['fastest lap driver'] = soup.find("span", {'class': 'typography-module_body-xs-semibold__Fyfwn text-text-3'}).get_text(strip=True).lower()
        
    return infos
