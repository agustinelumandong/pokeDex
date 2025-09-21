from bs4 import *
from urllib.request import *
from typing import *
from pymongo import *

url = 'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)

page = urlopen(request)
page_context_bytes = page.read()
page_html = page_context_bytes.decode('utf-8')
soup = BeautifulSoup(page_html, "html.parser")


poke_rows = soup.find_all("table", id = "pokedex")[0].find_all("tbody")[0].find_all("tr")

for poke_row in poke_rows[0:5]:
    poke_data = poke_row.find_all("td")

    # 1st column
    poke_id = poke_data[0].find_all("span")[0].getText()
    poke_name = poke_data[1].find_all("a")[0].getText()
    poke_avatar = poke_data[0].find_all("picture")[0].find_all("source")[0]["srcset"]
    poke_details_uri = poke_data[1].find_all("a")[0].find_all("a")
    types = []

    for poke_type in poke_data[2].find_all("a"):
        types.append(poke_type.getText())
    
    poke_stats_total = poke_data[3].getText()
    poke_hp = poke_data[4].getText()
    poke_atk = poke_data[5].getText()
    poke_def = poke_data[6].getText()
    poke_spAtk = poke_data[7].getText()
    poke_spDef = poke_data[8].getText()
    poke_speed = poke_data[9].getText()

    pokemon = {
        "number": poke_id,
        "name": poke_name,
        "poke-uri": poke_details_uri,
        "types": types,
        "stats": {
            "total": poke_stats_total,
            "hp": poke_hp,
            "attack": poke_atk,
            "defense": poke_def,
            "sp_atk": poke_spAtk,
            "sp_def": poke_spDef,
            "speed": poke_speed,
        }
    }


    entry_url = 'https://pokemondb.net/{poke_details_uri}'
    request = Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    entry_html_page = urlopen(request).read().decode('utf-8')
    entry_soup =BeautifulSoup(entry_html_page, "html.parser")
    entry_text = ""

    try:
        h2 = entry_soup.find("h2", string="Pokédex entries")

        if(h2):
            table = h2.find_next("table")
            if(table):
                entry_text = table.find("tr").find("td").get_text(strip=True)
            else:
                print(f"No table found under 'Pokédex entries' for {poke_name}")
        else:
            print(f"No 'Pokédex entries' section found for {poke_name} ")

    except Exception as e:
        print(f"Error while scraping entry for {poke_name}: {e} ")
        exit
        




