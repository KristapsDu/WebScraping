import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0'
}
base_url = 'https://www.ss.lv'

# Nosakām pilsētas ar rajoniem
citieswithdistricts = ["rīga", "rīgas rajons", "daugavpils un rajons", "jelgava un rajons", "liepāja un rajons"]

# Iegūstam pilsētu saites
main_url = f'{base_url}/lv/real-estate/flats/sell/'
response = requests.get(main_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

city_map = {}
categories = soup.find_all('h4', class_='category')
for cat in categories:  
    link = cat.find('a', class_='a_category')
    if link:
        city_name = link.text.strip()
        print(city_name)
        href = link['href']
        city_map[city_name.lower()] = href

user_city = input("Ievadi pilsētu: ").strip().lower()

if user_city in city_map:

    # Ielādējam lapu ar rajoniem
    riga_url = base_url + city_map[user_city]
    response = requests.get(riga_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    if any(element in user_city.lower() for element in citieswithdistricts):

        # Atrodam rajonus
        districts = {}
        categories = soup.find_all('h4', class_='category')
        for cat in categories:
            link = cat.find('a', class_='a_category')
            if link:
                district_name = link.text.strip()
                href = link['href']
                districts[district_name.lower()] = href

        # Parādam pieejamos rajonus
        print("\nPieejamie rajoni:")
        for name in districts:
            print("-", name.title())

        # Lietotājs izvēlas rajonu
        user_district = input("\nIevadi rajonu no saraksta: ").strip().lower()
        if user_district in districts:
            userdistrict = districts[user_district].replace(' ','-')
            full_url = base_url + districts[user_district]
        else:
            print("Rajons nav atrasts.")
            exit()

    else:
        # Parastajām pilsētām nav rajonu
        full_url = base_url + city_map[user_city]

    # Filtru ievadīšana

    #istabu skaits
    try:
        min_rooms = int(input("Ievadi minimālo istabu skaitu(1-6): "))
    except:
        min_rooms = None
        print("Filtrs netiks ieskaitīts")
    try:
        max_rooms = int(input("Ievadi maksimālo istabu skaitu(1-6): "))
    except:
        max_rooms = None
        print("Filtrs netiks ieskaitīts")

    # platība
    try:
        min_size = float(input("Ievadi minimālo platību: "))
    except:
        min_size = None
        print("Filtrs netiks ieskaitīts")
    try:
        max_size = float(input("Ievadi maksimālo platību: "))
    except:
        max_size = None
        print("Filtrs netiks ieskaitīts")

    # cena
    try:
        min_price = float(input("Ievadi minimālo cenu: "))
    except:
        min_price = None
        print("Filtrs netiks ieskaitīts")
    try:
        max_price = float(input("Ievadi maksimālo cenu: "))
    except:
        max_price = None
        print("Filtrs netiks ieskaitīts")

    # -----

    print(f"\nIelade sludinājumus no: {full_url}")
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    ad_listings = soup.find_all("tr", id=lambda x: x and x.startswith("tr_"))
    print(f"Atrastie sludinājumi: {len(ad_listings)}")

    for ad in ad_listings:
        cells = ad.find_all('td')
        if len(cells) >= 5:
            location = cells[3].text.strip()
            room_info = int(cells[4].text.strip())
            # istabu skaits
            if min_rooms == None or max_rooms == None:
                continue
            if room_info < min_rooms or room_info > max_rooms:
                continue
            # platiba
            size = float(cells[5].text.strip())
            if min_size == None or max_size == None:
                continue
            if size < min_size or size > max_size:
                continue
            #cena
            price = cells[-1].text.strip()
            if min_price == None or max_price == None:
                continue
            if price < min_price or price > max_price:
                continue

            print("Atrašanas vieta:", location)
            print("Istabas:", room_info)
            print("Platība:", size)
            print("Cena:", price)
            print("------")

else:
    print("Šada pilsēta nav atrasta sludinājumos.")
