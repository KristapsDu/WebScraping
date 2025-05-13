import requests
from bs4 import BeautifulSoup
import xlsxwriter

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
        if user_district == "visi":
            full_url = base_url + "all"
        elif user_district in districts:
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
        min_rooms = 0
        print("Filtrs netiks ieskaitīts")
    try:
        max_rooms = int(input("Ievadi maksimālo istabu skaitu(1-6): "))
    except:
        max_rooms = 6
        print("Filtrs netiks ieskaitīts")

    print()

    # platība
    try:
        min_size = float(input("Ievadi minimālo platību: "))
    except:
        min_size = 0
        print("Filtrs netiks ieskaitīts")
    try:
        max_size = float(input("Ievadi maksimālo platību: "))
    except:
        max_size = 100000
        print("Filtrs netiks ieskaitīts")
    
    print()

    # cena
    try:
        min_price = float(input("Ievadi minimālo cenu: "))
    except:
        min_price = 0
        print("Filtrs netiks ieskaitīts")
    try:
        max_price = float(input("Ievadi maksimālo cenu: "))
    except:
        max_price = 100000000
        print("Filtrs netiks ieskaitīts")

    print()

    # -----
    # lapu skaits
    try:
       pages = int(input("Ievadi cik lapas nolasīt: "))
    except:
       pages    = 0

    # -----

    print(f"\nIelade sludinājumus no: {full_url}")
    response = requests.get(full_url, headers=headers)

    workbook = xlsxwriter.Workbook('sludinajumi.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ["Atrašanās vieta", "Istabas", "Platība", "Cena (€)"])
    row = 1

    matching = 0

    currentpage = 1
    while currentpage <= pages:
        if currentpage == 1:
            url = full_url
        else:
            url = full_url.rstrip("/") + f"/page{currentpage}.html"

        print(f"\n ielade: {url}")
        response = requests.get(url, headers=headers)

        if response.url != url:
            print(f"\n Pieejamas tikai {currentpage-1} lapas")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        ad_listings = soup.find_all("tr", id=lambda x: x and x.startswith("tr_"))

        for ad in ad_listings:
            cells = ad.find_all('td')
            if len(cells) >= 5:
                try:
                    location = cells[3].text.strip()
                    room_info = int(cells[4].text.strip())
                    # istabu skaits
                    if room_info < min_rooms or room_info > max_rooms:
                        continue
                    # platiba
                    size = int(cells[5].text.strip())
                    if size < min_size or size > max_size:
                        continue
                    #cena
                    price = int(cells[-1].text.strip().replace("  €","").replace(",",""))
                    if price < min_price or price > max_price:
                        continue

                    print("Atrašanas vieta:", location)
                    print("Istabas:", room_info)
                    print("Platība:", size, "m2")
                    print("Cena:", price,"€")
                    print("------")

                    matching += 1
                    worksheet.write_row(row, 0, [location, room_info, size, price])
                    row += 1

                except:
                    print("Kļūda:")
                    continue

        currentpage +=1

    workbook.close()
    print("Ar kritērijiem sakrita "+str(matching)+"/"+str(len(ad_listings)+1))

else:
    print("Šada pilsēta nav atrasta sludinājumos.")
