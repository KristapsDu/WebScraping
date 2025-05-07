import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0'
}
base_url = 'https://www.ss.lv'

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
        href = link['href']
        city_map[city_name.lower()] = href

user_city = input("Ievadi pilsētu (piemēram: Rīga, Cēsis, Limbaži): ").strip().lower()

if user_city in city_map:
    if user_city == "rīga":
        # Ielādējam Rīgas lapu ar rajoniem
        riga_url = base_url + city_map[user_city]
        response = requests.get(riga_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Atrodam Rīgas rajonus
        riga_districts = {}
        categories = soup.find_all('h4', class_='category')
        for cat in categories:
            link = cat.find('a', class_='a_category')
            if link:
                district_name = link.text.strip()
                href = link['href']
                riga_districts[district_name.lower()] = href

        # Parādam pieejamos rajonus
        print("\nPieejamie Rīgas rajoni:")
        for name in riga_districts:
            print("-", name.title())

        # Lietotājs izvēlas rajonu
        user_district = input("\nIevadi rajonu no saraksta: ").strip().lower()
        if user_district in riga_districts:
            full_url = base_url + riga_districts[user_district]
        else:
            print("Rajons nav atrasts.")
            exit()

    else:
        # Parastajām pilsētām nav rajonu
        full_url = base_url + city_map[user_city]

    print(f"\nIelādēju sludinājumus no: {full_url}")
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    ad_listings = soup.find_all("tr", id=lambda x: x and x.startswith("tr_"))
    print(f"Atrastie sludinājumi: {len(ad_listings)}")

    for ad in ad_listings:
        cells = ad.find_all('td')
        if len(cells) >= 5:
            location = cells[3].text.strip()
            room_info = cells[4].text.strip()
            size = cells[5].text.strip()
            price = cells[-1].text.strip()

            print("Lokācija:", location)
            print("Istabas:", room_info)
            print("Platība:", size)
            print("Cena:", price)
            print("------")

else:
    print("Šāda pilsēta nav atrasta sludinājumos.")
