# WebScraping projekts
Autori: Kristaps Duļbinskis 241RDB253 un Kārlis Zvirbulis 241RDB082

## Projekta uzdevums
Projekta uzdevums ir nolasīt un saglabāt nekustamā īpašuma pārdošanas sludinājumus no mājaslapas ss.lv. Ar kodu ir iespējams atrast dzīvokļu, privātmāju un lauku viensētu sludinājumus.
Katru īpašuma veidu atlasa sīkāk pa pilsētām, to rajoniem un apakšrajoniem, ja nepieciešams. Vēl pie tā, var izvēlēties cenu, platības un istabu vai stāvu skaitu, atkarībā no kāda veida īpašumi tiek nolasīti. Iespējams arī noteikt cik lapas nolasīt.
Visi rezultāti, kas sakrīt ar noteiktajiem kritērijiem, tiek saglabāti .xlsx failā ar nosaukumiem, kas atkarīgi no īpašuma tipa, pilsētas vai rajona un apakšrajoniem.

## Lietotās Python bibliotēkas
Programmas izveidošanai izmantojām 3 bibliotēkas:
### Requests
_Requests_ ir bibliotēka ar kuru var vieglāk veikt HTTP pieprasījummus. Ar šo bibliotēku mēs samazinājām nepieciešamo pieprasijumu kodu.
### BeautifulSoup4
_BeautifulSoup4_ tiek lietota, lai iegūtu datus no HTML failiem, kuri atrodas mājaslapās. Šī bibliotēka ir nepieciešama, lai vispār projekta webscraping daļa būtu iespējama.
### xlsxwriter
_xlsxwriter_ iespejo mums saglabāt iegūtos datus Excel failu formātā, ar kuru ir iespējams pēc tam apstrādāt iegūtos datu ar salīdzināšanu, maksimumālo un minimālo vērtību noteikšanu un citu veidu datu apstrādi.

## Projekta izstrādes laikā izmantotās pašu definētās datu struktūras
Projektā izmantojam tabulu datu glabāšanai, kas ir __divdimensiāls masīvs__ _(two-dimensional array)_. Šo datu struktūru izmantojām, lai saistītu viena sludinājuma datus vienu ar otru un šos saistītos datus apvienotu vienā vietā ar citiem datiem.

## Programmatūras izmantošana
Pirms programmas palaišanas ir nepieciešams, ka lietojat vismaz Python 3.10 un ir instalētas 'requests', 'beautifulsoup4' un 'xlsxwriter' bibliotēkas. Bibliotēku instalēšanas instrukcijas pieejamas [šeit](https://packaging.python.org/en/latest/tutorials/installing-packages/). 

Lietojot programmatūru, ierakstot kādu piedāvāto izvēli, nav obligāti jaievēro lielie burti. Jaievada pilns teksts, ievērojot garumzīmes, atstarpes un punktus.

Ieslēdzot programmu, būs pieejamas 3 īpašumu izvēles: Dzīvokļi, mājas un vasarnīcas un lauku viensētas.
Pēc īpasuma veids ir izvēlēts, nepieciešams izvēlēties pilsētu kā arī kādu no tās rajoniem, ja tie parādās pēc pilsētas izvēles veikšanas.
Būs iespēja izvēlēties maksimālās un minimālās vērtības intervāliem, pēc kuriem saglabās sludinājumu datus. Atkarībā no kuru īpašuma izvēlējaties sākuma, būs pieejami atšķirīgi kritērīji. No ievadītajām vērtībām tiks reģistrēti tikai skaitļi. Ievadot burtus vai tukšumu vērtību vietā iestatīs kā to noklusējuma vērtības.

### Noklusējumu vērtības:
 - Minimālais istabu skaits - 0  
 - Maksimālais istabu skaits - 10  
 - Minimālais stāvu skaits - 0  
 - Maksimālais stāvu skaits - 10  
 - Minimālā platība - 0  
 - Maksimālā platība - 100,000 m2  
 - Minimālā cena - 0  
 - Maksimālā cena - 100,000,000 €  

Pēc kritēriju noteikšanai, ir jaizvēlas cik lapas, ja iespējams, it janolasa. Nolasīto lapu noklusējuma vērtība ir <ins>1 lapa</ins>.
Nolasītie sludinājumi, kas atbilst visiem noteiktajiem kritērijiem, tiks izvadīti un saglabāti .xlsx failā <ins>tajā pašā adresē, kur programmatūras fails atrodas</ins>.

### Lietošanas video piemērs
[![Video](https://i9.ytimg.com/vi/TQr379_-4nE/mqdefault.jpg?sqp=COS0kcEG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGGUgXCguMA8=&rs=AOn4CLALA8Q10wN3xs1ues9mNz99ZARAFQ)](https://youtu.be/TQr379_-4nE)
