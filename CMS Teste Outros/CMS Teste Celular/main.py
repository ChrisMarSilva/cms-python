from loguru import logger
import datetime as dt
import time
import phonenumbers
from phonenumbers import carrier
import folium
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()
        
        # number = "+442083661177"
        # region = None
        # ch_number = phonenumbers.parse(number=number, region=region)
        # print(ch_number)
        
        # number = "+5511942124681"
        # region = None
        # ch_number = phonenumbers.parse(number=number, region=region)
        # print(ch_number)

        # number = "0431234567"
        # region = "CH"
        # ch_number = phonenumbers.parse(number=number, region=region)
        # print(ch_number)
        # description = geocoder.description_for_number(numobj=ch_number, lang="de")
        # print(description)

        # number = "+5511942124681"
        # region = "br"
        # ch_number = phonenumbers.parse(number=number, region=region)
        # print(ch_number)
        # description = geocoder.description_for_number(numobj=ch_number, lang="pt-br")
        # print(description)
        # carr = carrier.name_for_number(numobj=ch_number, lang="pt-br")
        # print("carr", carr)

        # text = "Call me at 510-748-8230 if it's before 9:30, or on 703-4800500 after 10am."
        # for match in phonenumbers.PhoneNumberMatcher(text, "US"):
        #     print(match)

        number = "+5511942124681"
        
        pepnumber = phonenumbers.parse(number=number)
        logger.info(f"{pepnumber}")

        from phonenumbers import geocoder

        location = geocoder.description_for_number(numobj=pepnumber, lang="br")
        logger.info(f"{location}")
        
        service_pro = phonenumbers.parse(number=number)
        carr = carrier.name_for_number(numobj=service_pro, lang="en")  # pt-br
        logger.info(f"{carr}")

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

        import opencage
        from opencage.geocoder import OpenCageGeocode
        from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError
        geo = OpenCageGeocode(key='090d7cd97d8944ff8c9342f2920b648e')
        results = geo.geocode(query=str(location))
        # results = geo.reverse_geocode(44.8303087, -0.5761911) 
        # results = geocoder.reverse_geocode(44.8303087, -0.5761911, language='de', no_annotations='1')

        # logger.info(f"{results}")

        # [{'annotations': {'DMS': {'lat': "23° 33' 2.34252'' S", 'lng': "46° 38' 0.17664'' W"}, 'MGRS': '23KLP3327994571', 'Maidenhead': 'GG66qk37xu', 'Mercator': {'x': -5191204.383, 'y': -2681681.409}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?node=30674098#map=16/-23.55065/-46.63338', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-23.55065/-46.63338&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-23.55065&mlon=-46.63338#map=16/-23.55065/-46.63338'}, 'UN_M49': {'regions': {'AMERICAS': '019', 'BR': '076', 'LATIN_AMERICA': '419', 'SOUTH_AMERICA': '005', 'WORLD': 
        # '001'}, 'statistical_groupings': ['LEDC']}, 'callingcode': 55, 'currency': {'decimal_mark': ',', 'html_entity': 'R$', 'iso_code': 
        # 'BRL', 'iso_numeric': '986', 'name': 'Brazilian Real', 'smallest_denomination': 5, 'subunit': 'Centavo', 'subunit_to_unit': 100, 'symbol': 'R$', 'symbol_first': 1, 'thousands_separator': '.'}, 'flag': '🇧🇷', 'geohash': '6gyf4bdxe  2tb3y6sy0ey', 'qibla': 68.94, 
        # 'roadinfo': {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650360180, 'astronomical': 1650355620, 'civil': 1650358800, 'nautical': 1650357240}, 'set': {'apparent': 1650401280, 'astronomical': 1650405840, 'civil': 1650402660, 'nautical': 1650404220}}, 'timezone': {'name': 'America/Sao_Paulo', 'now_in_dst': 0, 'offset_sec': -10800, 'offset_string': '-0300', 'short_name': 'BRT'}, 'what3words': {'words': 'among.caller.caskets'}, 'wikidata': 'Q174'}, 'bounds': {'northeast': {'lat': -23.3906507, 'lng': -46.4733824}, 'southwest': {'lat': -23.7106507, 'lng': -46.7933824}}, 'components': {'ISO_3166-1_alpha-2': 'BR', 'ISO_3166-1_alpha-3': 'BRA', '_category': 'place', '_type': 'city', 'city': 'São Paulo', 'continent': 'South America', 'country': 'Brazil', 'country_code': 'br', 'county': 'Região Metropolitana de São Paulo', 'municipality': 'Região Imediata de São Paulo', 'postcode': 
        # '01001-000', 'region': 'Southeast Region', 'state': 'São Paulo', 'state_code': 'SP', 'state_district': 'Região Geográfica Intermediária de São Paulo'}, 'confidence': 3, 'formatted': 'São Paulo, Região Metropolitana de São Paulo, Brazil', 'geometry': {'lat': -23.5506507, 'lng': -46.6333824}}, {'annotations': {'DMS': {'lat': "23° 40' 57.53280'' S", 'lng': "46° 43' 0.49116'' W"}, 'MGRS': '23KLP2493879854', 'Maidenhead': 'GG66ph36xd', 'Mercator': {'x': -5200490.734, 'y': -2697628.221}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?relation=298285#map=16/-23.68265/-46.71680', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-23.68265/-46.71680&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-23.68265&mlon=-46.71680#map=16/-23.68265/-46.71680'}, 'UN_M49': {'regions': {'AMERICAS': '019', 'BR': '076', 'LATIN_AMERICA': '419', 'SOUTH_AMERICA': '005', 'WORLD': '001'}, 'statistical_groupings': ['LEDC']}, 'callingcode': 55, 'currency': {'decimal_mark': ',', 'html_entity': 'R$', 'iso_code': 'BRL', 'iso_numeric': '986', 'name': 'Brazilian Real', 'smallest_denomination': 5, 'subunit': 'Centavo', 'subunit_to_unit': 100, 'symbol': 'R$', 'symbol_first': 1, 'thousands_separator': '.'}, 'flag': '🇧🇷', 'geohash': '6gyc2btyed6vfhkf3vhu', 'qibla'  : 68.98, 'roadinfo': {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650360180, 'astronomical': 1650355680, 'civil': 1650358800, 'nautical': 1650357240}, 'set': {'apparent': 1650401280, 'astronomical': 1650405840, 'civil': 1650402660, 'nautical': 1650404280}}, 'timezone': {'name': 'America/Sao_Paulo', 'now_in_dst': 0, 'offset_sec': -10800, 'offset_string': '-0300', 'short_name': 'BRT'}, 'what3words': {'words': 'wink.backlog.mouth'}, 'wikidata': 'Q174'}, 'bounds': {'northeast': {'lat': -23.3577551, 'lng': -46.3650898}, 'southwest': {'lat': -24.0079003, 'lng': -46.8262906}}, 'components': {'ISO_3166-1_alpha-2': 'BR', 'ISO_3166-1_alpha-3': 'BRA', '_category': 'place', '_type': 'city', 'city': 'São Paulo', 'continent': 'South America', 'country': 'Brazil', 'country_code': 'br', 
        # 'county': 'Região Metropolitana de São Paulo', 'municipality': 'Região Imediata de São Paulo', 'region': 'Southeast Region', 'state': 'São Paulo', 'state_code': 'SP', 'state_district': 'Região Geográfica Intermediária de São Paulo'}, 'confidence': 1, 'formatted': 'São Paulo, Região Metropolitana de São Paulo, Brazil', 'geometry': {'lat': -23.682648, 'lng': -46.7168031}}, {'annotations': 
        # {'DMS': {'lat': "22° 4' 12.97380'' S", 'lng': "48° 26' 0.19500'' W"}, 'MGRS': '22KGA6486157164', 'Maidenhead': 'GG57sw73xd', 'Mercator': {'x': -5391580.034, 'y': -2503915.712}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?relation=298204#map=16/-22.07027/-48.43339', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-22.07027/-48.43339&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-22.07027&mlon=-48.43339#map=16/-22.07027/-48.43339'}, 'UN_M49': {'regions': {'AMERICAS': '019', 'BR': '076', 'LATIN_AMERICA': '419', 'SOUTH_AMERICA': '005', 'WORLD': '001'}, 'statistical_groupings': ['LEDC']}, 'callingcode': 55, 'currency': {'decimal_mark': ',', 'html_entity': 'R$', 'iso_code': 'BRL', 'iso_numeric': '986', 'name': 'Brazilian Real', 'smallest_denomination': 5, 'subunit': 'Centavo', 'subunit_to_unit': 100, 'symbol': 'R$', 'symbol_first': 1, 'thousands_separator': '.'}, 'flag': 
        # '🇧🇷', 'geohash': '6ujd3y5zk72sr4jv5v03', 'qibla': 69.43, 'roadinfo': {'drive_on': 'right', 'speed_  in': 'km/h'}, 'sun': {'rise': 
        # {'apparent': 1650360540, 'astronomical': 1650356040, 'civil': 1650359160, 'nautical': 1650357600}, 'set': {'apparent': 1650401820, 'astronomical': 1650406260, 'civil': 1650403140, 'nautical': 1650404700}}, 'timezone': {'name': 'America/Sao_Paulo', 'now_in_dst': 0, 'offset_sec': -10800, 'offset_string': '-0300', 'short_name': 'BRT'}, 'what3words': {'words': 'doormats.friction.inboxes'}, 'wikidata': 'Q175'}, 'bounds': {'northeast': {'lat': -19.7823272, 'lng': -44.161}, 'southwest': {'lat': -25.4832679, 'lng': -53.109}}, 'components': {'ISO_3166-1_alpha-2': 'BR', 'ISO_3166-1_alpha-3': 'BRA', '_category': 'place', '_type': 'state', 'continent': 'South America', 'country': 'Brazil', 'country_code': 'br', 'region': 'Southeast Region', 'state': 'São Paulo', 'state_code': 'SP'}, 'confidence': 1, 'formatted': 'São Paulo, Brazil', 'geometry': {'lat': -22.0702705, 'lng': -48.4333875}}, {'annotations': {'DMS': {'lat': "39° 47' 16.86444'' N", 'lng': "8° 17' 27.75624'' W"}, 'MGRS': '29SNE6070304470', 'Maidenhead': 'IM59us59bc', 'Mercator': {'x': -922954.729, 'y': 4807835.921}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?node=5584337892#map=16/39.78802/-8.29104', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/39.78802/-8.29104&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=39.78802&mlon=-8.29104#map=16/39.78802/-8.29104'}, 'UN_M49': {'regions': {'EUROPE': '150', 'PT': '620', 'SOUTHERN_EUROPE': '039', 'WORLD': '001'}, 'statistical_groupings': ['MEDC']}, 'callingcode': 351, 'currency': {'alternate_symbols': [], 'decimal_mark': ',', 'html_entity': '&#x20AC;', 'iso_code': 'EUR', 'iso_numeric': '978', 'name': 'Euro', 'smallest_denomination': 1, 'subunit': 'Cent', 'subunit_to_unit': 100, 'symbol': '€', 'symbol_first': 0, 'thousands_separator': '.'}, 'flag': '🇵🇹', 'geohash': 'e  
        # z44774wh8jgwxen62f6', 'qibla': 99.59, 'roadinfo': {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650347460, 'astronomical': 1650341640, 'civil': 1650345780, 'nautical': 1650343740}, 'set': {'apparent': 1650395640, 'astronomical': 1650401520, 'civil': 1650397320, 'nautical': 1650399360}}, 'timezone': {'name': 'Europe/Lisbon', 'now_in_dst': 1, 'offset_sec': 3600, 
        # 'offset_string': '+0100', 'short_name': 'WEST'}, 'what3words': {'words': 'drivel.unfortunate.editing'}}, 'bounds': {'northeast': {'lat': 39.7880679, 'lng': -8.2909934}, 'southwest': {'lat': 39.7879679, 'lng': -8.2910934}}, 'components': {'ISO_3166-1_alpha-2': 
        # 'PT', 'ISO_3166-1_alpha-3': 'PRT', '_category': 'natural/water', '_type': 'peak', 'continent': 'Europe', 'country': 'Portugal', 'country_code': 'pt', 'county': 'Santarém', 'county_code': 'STR', 'peak': 'São Paulo', 'political_union': 'European Union', 'postcode': '2240-612', 'town': 'Ferreira do Zêzere'}, 'confidence': 9, 'formatted': 'São Paulo, 2240-612 Ferreira do Zêzere, Portugal', 'geometry': {'lat': 39.7880179, 'lng': -8.2910434}}, {'annotations': {'DMS': {'lat': "8° 48' 48.68892'' S", 'lng': "13° 15' 21.32028'' E"}, 'MGRS': '33LUL0817525316', 'Maidenhead': 'JI61pe04rs', 'Mercator': {'x': 1475642.52, 'y': -978466.908}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?node=769989730#map=16/-8.81352/13.25592', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-8.81352/13.25592&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-8.81352&mlon=13.25592#map=16/-8.81352/13.25592'}, 'UN_M49': {'regions': {'AFRICA': '002', 'AO': '024', 'MIDDLE_AFRICA': '017', 'SUB-SAHARAN_AFRICA': '202', 'WORLD': '001'}, 'statistical_groupings': ['LDC', 'LEDC']}, 'callingcode': 244, 'currency': {'alternate_symbols': [], 'decimal_mark': '.', 'format': '%n %u', 'html_entity': '', 'iso_code': 'AOA', 'iso_numeric': '973', 'name': 'Angolan Kwanza', 'smallest_denomination': 10, 'subunit': 'Cêntimo', 'subunit_to_unit': 100, 'symbol': 'Kz', 'symbol_first': 0, 'thousands_separator': ','}, 'flag': '🇦🇴', 'geohash':   
        # 'kq3mves9mruj63msj52h', 'qibla': 40.44, 'roadinfo': {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650345060, 'astronomical': 1650340800, 'civil': 1650343740, 'nautical': 1650342300}, 'set': {'apparent': 1650387660, 'astronomical': 1650391920, 'civil': 1650388980, 'nautical': 1650390420}}, 'timezone': {'name': 'Africa/Lagos', 'now_in_dst': 0, 'offset_sec': 3600, 'offset_string': '+0100', 'short_name': 'WAT'}, 'what3words': {'words': 'remember.uptake.dome'}}, 'bounds': {'northeast': {'lat': -8.7935247, 'lng': 13.2759223}, 'southwest': {'lat': -8.8335247, 'lng': 13.2359223}}, 'components': {'ISO_3166-1_alpha-2': 'AO', 
        # 'ISO_3166-1_alpha-3': 'AGO', '_category': 'place', '_type': 'neighbourhood', 'city': 'Luanda', 'continent': 'Africa', 'country': 'Angola', 'country_code': 'ao', 'county': 'Municipality of Luanda', 'district': 'Sambizanga Urban District', 'postcode': '3141', 'state': 'Luanda Province', 'suburb': 'São Paulo'}, 'confidence': 7, 'formatted': 'Luanda, 3141, Angola', 'geometry': {'lat': -8.8135247, 'lng': 13.2559223}}, {'annotations': {'DMS': {'lat': "14° 31' 51.27420'' S", 'lng': "40° 22' 37.46496'' W"}, 'MGRS': '24LUJ5162393109', 'Maidenhead': 'GH95tl42sn', 'Mercator': {'x': -4494755.273, 'y': -1624483.302}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?node=2780171579#map=16/-14.53091/-40.37707', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-14.53091/-40.37707&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-14.53091&mlon=-40.37707#map=16/-14.53091/-40.37707'}, 'UN_M49': {'regions': {'AMERICAS': '019', 'BR': '076', 'LATIN_AMERICA': '419', 'SOUTH_AMERICA': '005', 'WORLD': '001'}, 'statistical_groupings': ['LEDC']}, 'callingcode': 55, 'currency': {'decimal_mark': ',', 'html_entity': 'R$', 'iso_code': 'BRL', 'iso_numeric': '986', 'name': 'Brazilian Real', 'smallest_denomination': 5, 'subunit': 'Centavo', 'subunit_to_unit': 100, 'symbol': 'R$', 'symbol_first': 1, 'thousands_separator': '.'}, 'flag': '🇧🇷', 'geohash': '7j7m34wr3fpu2xcdzfdc', 'qibla': 66.  79, 'roadinfo': {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650358200, 'astronomical': 1650353880, 'civil': 1650356880, 'nautical': 1650355380}, 'set': {'apparent': 1650400260, 'astronomical': 1650404580, 'civil': 1650401580, 'nautical': 1650403080}}, 'timezone': {'name': 'America/Bahia', 'now_in_dst': 0, 'offset_sec': -10800, 'offset_string': '-0300', 'short_name': '-03'}, 'what3words': 
        # {'words': 'breathy.hornless.obeyed'}}, 'bounds': {'northeast': {'lat': -14.5109095, 'lng': -40.3570736}, 'southwest': {'lat': -14.5509095, 'lng': -40.3970736}}, 'components': {'ISO_3166-1_alpha-2': 'BR', 'ISO_3166-1_alpha-3': 'BRA', '_category': 'place', '_type': 'neighbourhood', 'city_district': 'Poções', 'continent': 'South America', 'country': 'Brazil', 'country_code': 'br', 'municipality': 'Região Geográfica Imediata de Vitória da Conquista', 'postcode': '45260-000', 'region': 'Northeast Region', 'state': 'Bahia', 'state_code': 'BA', 'state_district': 'Região Geográfica Intermediária de Vitória da Conquista', 'suburb': 'São Paulo', 'town': 'Poções'}, 'confidence': 7, 'formatted': 'São Paulo, Poções - BA, 45260-000, Brazil', 'geometry': {'lat': -14.5309095, 'lng': -40.3770736}}, {'annotations': {'DMS': {'lat': "10° 6' 27.91872'' S", 'lng': "39° 29' 43.39680'' W"}, 'MGRS': '24LVP4572582632', 'Maidenhead': 'HH09gv04nd', 'Mercator': {'x': -4396606.481, 'y': -1123578.346}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?node=4991289574#map=16/-10.10776/-39.49539', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-10.10776/-39.49539&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-10.10776&mlon=-39.49539#map=16/-10.10776/-39.49539'}, 'UN_M49': {'regions': {'AMERICAS': '019', 'BR': '076', 'LATIN_AMERICA': '419', 'SOUTH_AMERICA': '005', 'WORLD': '001'}, 'statistical_groupings': ['LEDC']}, 'callingcode': 55, 'currency': {'decimal_mark': ',', 'html_entity': 'R$', 'iso_code': 'BRL', 'iso_numeric': '986', 'name': 'Brazilian Real', 'smallest_denomination': 5, 'subunit': 'Centavo', 'subunit_to_unit': 100, 'symbol': 'R$', 'symbol_first': 1, 'thousands_separator': '.'}, 'flag': '🇧🇷', 'geohash': '7n5ymrbq4cb5wkmwr021', 'qibla': 66.92, 'roadinfo':   {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650357780, 'astronomical': 1650353520, 'civil': 1650356460, 'nautical': 1650355020}, 'set': {'apparent': 1650400260, 'astronomical': 1650404520, 'civil': 1650401580, 'nautical': 1650403020}}, 'timezone': {'name': 'America/Bahia', 'now_in_dst': 0, 'offset_sec': -10800, 'offset_string': '-0300', 'short_name': '-03'}, 'what3words': {'words': 'unblocked.extracting.uncrowded'}}, 'bounds': {'northeast': {'lat': -10.0877552, 'lng': -39.475388}, 'southwest': {'lat': -10.1277552, 
        # 'lng': -39.515388}}, 'components': {'ISO_3166-1_alpha-2': 'BR', 'ISO_3166-1_alpha-3': 'BRA', '_category': 'place', '_type': 'village', 'continent': 'South America', 'country': 'Brazil', 'country_code': 'br', 'municipality': 'Região Geográfica Imediata de Juazeiro', 'region': 'Northeast Region', 'state': 'Bahia', 'state_code': 'BA', 'state_district': 'Região Geográfica Intermediária de Juazeiro', 'town': 'Uauá', 'village': 'São Paulo'}, 'confidence': 7, 'formatted': 'Uauá, Região Geográfica Intermediária de Juazeiro, Brazil', 'geometry': {'lat': -10.1077552, 'lng': -39.495388}}, {'annotations': {'DMS': {'lat': "28° 43' 47.63568'' S", 'lng': "51° 48' 30.20688'' W"}, 'MGRS': '22JDP2105721670', 'Maidenhead': 'GG41cg24xt', 'Mercator': {'x': -5767283.683, 'y': -3320778.357}, 
        # 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?node=8664292708#map=16/-28.72990/-51.80839', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-28.72990/-51.80839&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-28.72990&mlon=-51.80839#map=16/-28.72990/-51.80839'}, 'UN_M49': {'regions': {'AMERICAS': '019', 'BR': '076', 'LATIN_AMERICA': '419', 'SOUTH_AMERICA': '005', 'WORLD': '001'}, 'statistical_groupings': ['LEDC']}, 'callingcode': 55, 'currency': {'decimal_mark': ',', 'html_entity': 'R$', 
        # 'iso_code': 'BRL', 'iso_numeric': '986', 'name': 'Brazilian Real', 'smallest_denomination': 5, 'subunit': 'Centavo', 'subunit_to_unit': 100, 'symbol': 'R$', 'symbol_first': 1, 'thousands_separator': '.'}, 'flag': '🇧🇷', 'geohash'  : '6fght1fk0yxy5ekscwwe', 'qibla': 71.71, 'roadinfo': {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650361740, 'astronomical': 1650357000, 'civil': 1650360300, 'nautical': 1650358620}, 'set': {'apparent': 1650402240, 'astronomical': 1650406980, 'civil': 1650403680, 'nautical': 1650405300}}, 'timezone': {'name': 'America/Sao_Paulo', 'now_in_dst': 0, 'offset_sec': -10800, 'offset_string': '-0300', 'short_name': 'BRT'}, 'what3words': {'words': 'droopy.withstood.predict'}}, 'bounds': {'northeast': {'lat': -28.7098988, 'lng': -51.7883908}, 'southwest': {'lat': -28.7498988, 'lng': -51.8283908}}, 'components': {'ISO_3166-1_alpha-2': 'BR', 'ISO_3166-1_alpha-3': 'BRA', '_category': 'place', '_type': 'neighbourhood', 'city_district': 'Nova Bassano', 'continent': 'South America', 'country': 'Brazil', 'country_code': 'br', 'municipality': 'Região Geográfica Imediata de Nova Prata - Guaporé', 'region': 'South Region', 'state': 'Rio Grande do Sul', 'state_code': 'RS', 'state_district': 'Região Geográfica Intermediária de Caxias do Sul', 'suburb': 'São Paulo', 'town': 'Nova Bassano'}, 'confidence': 7, 'formatted': 'São Paulo, Nova Bassano, Região Geográfica Intermediária de Caxias do Sul, Brazil', 'geometry': {'lat': -28.7298988, 'lng': -51.8083908}}, {'annotations': {'DMS': {'lat': "29° 31' 23.95488'' S", 'lng': "49° 52' 4.74924'' W"}, 'MGRS': '22JFN0970133498', 'Maidenhead': 'GG50bl54uj', 'Mercator': {'x': -5551278.797, 'y': -3421371.285}, 'OSM': {'edit_url': 'https://www.openstreetmap.org/edit?node=5275763680#map=16/-29.52332/-49.86799', 'note_url': 'https://www.openstreetmap.org/note/new#map=16/-29.52332/-49.86799&layers=N', 'url': 'https://www.openstreetmap.org/?mlat=-29.52332&mlon=-49.86799#map=16/-29.52332/-49.86799'}, 'UN_M49': {'regions': {'AMERICAS': '019', 'BR': '076', 'LATIN_AMERICA': '419', 'SOUTH_AMERICA': '005', 'WORLD': '001'}, 'statistical_groupings': ['LEDC']}, 'callingcode': 55, 'currency': {'decimal_mark': ',', 'html_entity': 'R$', 'iso_code': 'BRL', 'iso_numeric': '986', 'name': 'Brazilian Real', 'smallest_denomination': 5, 'subunit': 'Centavo', 'subunit_to_unit': 100, 'symbol': 'R$', 'symbol_first': 1, 'thousands_separator': '.'}, 'flag': '🇧🇷', 'geohash': '6fu811rnp  
        # wnes08kuh22', 'qibla': 71.01, 'roadinfo': {'drive_on': 'right', 'speed_in': 'km/h'}, 'sun': {'rise': {'apparent': 1650361320, 'astronomical': 1650356520, 'civil': 1650359820, 'nautical': 1650358200}, 'set': {'apparent': 1650401700, 'astronomical': 1650406500, 
        # 'civil': 1650403140, 'nautical': 1650404820}}, 'timezone': {'name': 'America/Sao_Paulo', 'now_in_dst': 0, 'offset_sec': -10800, 'offset_string': '-0300', 'short_name': 'BRT'}, 'what3words': {'words': 'unjust.revels.cooked'}}, 'bounds': {'northeast': {'lat': -29.5033208, 'lng': -49.8479859}, 'southwest': {'lat': -29.5433208, 'lng': -49.8879859}}, 'components': {'ISO_3166-1_alpha-2': 'BR', 'ISO_3166-1_alpha-3': 'BRA', '_category': 'place', '_type': 'neighbourhood', 'city_district': 'Arroio do Sal', 'continent': 'South America', 'country': 'Brazil', 'country_code': 'br', 'county': 'Aglomeração Urbana do Litoral Norte', 'municipality': 'Região Geográfica Imediata de Torres', 'postcode': '95585-000', 'region': 'South Region', 'state': 'Rio Grande do Sul', 'state_code': 'RS', 'state_district': 'Região Geográfica Intermediária de Porto Alegre', 'suburb': 'São Paulo', 'town': 'Arroio do Sal'}, 'confidence': 7, 'formatted': 'São Paulo, Arroio do Sal - RS, 95585-000, Brazil', 'geometry': {'lat': -29.5233208, 'lng': -49.8679859}}]

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        country = results[0]['components']['country_code']
        timezone = results[0]['annotations']['timezone']['name']

        logger.info(f"{lat=}")
        logger.info(f"{lng=}")
        logger.info(f"{country=}")
        logger.info(f"{timezone=}")

        m = folium.Map(location=[lat, lng], zoom_start=9)
        folium.Marker([lat, lng], popup=location, tooltip="Sua Localização").add_to(m)
        m.save("index.html")

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv

# python -m pip install --upgrade phonenumbers
# python -m pip install --upgrade opencage
# pip3 install opencage
# python -m pip install --upgrade folium


# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py