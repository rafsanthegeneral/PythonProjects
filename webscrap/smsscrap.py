from bs4 import BeautifulSoup
import requests
import random
import urllib.parse
import threading
import re

country_codes = {
    "+376": "AD",  # Andorra
    "+971": "AE",  # United Arab Emirates
    "+93": "AF",  # Afghanistan
    "+1-268": "AG",  # Antigua and Barbuda
    "+1-264": "AI",  # Anguilla
    "+355": "AL",  # Albania
    "+374": "AM",  # Armenia
    "+599": "AN",  # Netherlands Antilles
    "+244": "AO",  # Angola
    "+672": "AQ",  # Antarctica
    "+54": "AR",  # Argentina
    "+1-684": "AS",  # American Samoa
    "+43": "AT",  # Austria
    "+61": "AU",  # Australia
    "+297": "AW",  # Aruba
    "+358": "AX",  # Åland Islands
    "+994": "AZ",  # Azerbaijan
    "+387": "BA",  # Bosnia and Herzegovina
    "+1-246": "BB",  # Barbados
    "+880": "BD",  # Bangladesh
    "+32": "BE",  # Belgium
    "+226": "BF",  # Burkina Faso
    "+359": "BG",  # Bulgaria
    "+973": "BH",  # Bahrain
    "+257": "BI",  # Burundi
    "+229": "BJ",  # Benin
    "+590": "BL",  # Saint Barthélemy
    "+1-441": "BM",  # Bermuda
    "+673": "BN",  # Brunei Darussalam
    "+591": "BO",  # Bolivia
    "+599": "BQ",  # Bonaire, Sint Eustatius and Saba
    "+55": "BR",  # Brazil
    "+1-242": "BS",  # Bahamas
    "+975": "BT",  # Bhutan
    "+47": "BV",  # Bouvet Island
    "+267": "BW",  # Botswana
    "+375": "BY",  # Belarus
    "+501": "BZ",  # Belize
    "+1": "CA",  # Canada
    "+61": "CC",  # Cocos (Keeling) Islands
    "+243": "CD",  # Congo, The Democratic Republic Of The
    "+236": "CF",  # Central African Republic
    "+242": "CG",  # Congo
    "+41": "CH",  # Switzerland
    "+225": "CI",  # Côte D'Ivoire
    "+682": "CK",  # Cook Islands
    "+56": "CL",  # Chile
    "+237": "CM",  # Cameroon
    "+86": "CN",  # China
    "+57": "CO",  # Colombia
    "+506": "CR",  # Costa Rica
    "+53": "CU",  # Cuba
    "+238": "CV",  # Cape Verde
    "+599": "CW",  # Curaçao
    "+61": "CX",  # Christmas Island
    "+357": "CY",  # Cyprus
    "+420": "CZ",  # Czech Republic
    "+49": "DE",  # Germany
    "+253": "DJ",  # Djibouti
    "+45": "DK",  # Denmark
    "+1-767": "DM",  # Dominica
    "+1-809": "DO",  # Dominican Republic
    "+213": "DZ",  # Algeria
    "+593": "EC",  # Ecuador
    "+372": "EE",  # Estonia
    "+20": "EG",  # Egypt
    "+212": "EH",  # Western Sahara
    "+291": "ER",  # Eritrea
    "+34": "ES",  # Spain
    "+251": "ET",  # Ethiopia
    "+358": "FI",  # Finland
    "+679": "FJ",  # Fiji
    "+500": "FK",  # Falkland Islands (Malvinas)
    "+691": "FM",  # Micronesia, Federated States Of
    "+298": "FO",  # Faroe Islands
    "+33": "FR",  # France
    "+241": "GA",  # Gabon
    "+44": "GB",  # United Kingdom
    "+1-473": "GD",  # Grenada
    "+995": "GE",  # Georgia
    "+594": "GF",  # French Guiana
    "+44": "GG",  # Guernsey
    "+233": "GH",  # Ghana
    "+350": "GI",  # Gibraltar
    "+299": "GL",  # Greenland
    "+220": "GM",  # Gambia
    "+224": "GN",  # Guinea
    "+590": "GP",  # Guadeloupe
    "+240": "GQ",  # Equatorial Guinea
    "+30": "GR",  # Greece
    "+500": "GS",  # South Georgia and the South Sandwich Islands
    "+502": "GT",  # Guatemala
    "+1-671": "GU",  # Guam
    "+245": "GW",  # Guinea-Bissau
    "+592": "GY",  # Guyana
    "+852": "HK",  # Hong Kong
    "+61": "HM",  # Heard and McDonald Islands
    "+504": "HN",  # Honduras
    "+385": "HR",  # Croatia
    "+509": "HT",  # Haiti
    "+36": "HU",  # Hungary
    "+62": "ID",  # Indonesia
    "+353": "IE",  # Ireland
    "+972": "IL",  # Israel
    "+44": "IM",  # Isle of Man
    "+91": "IN",  # India
    "+246": "IO",  # British Indian Ocean Territory
    "+964": "IQ",  # Iraq
    "+98": "IR",  # Iran, Islamic Republic Of
    "+354": "IS",  # Iceland
    "+39": "IT",  # Italy
    "+44": "JE",  # Jersey
    "+1-876": "JM",  # Jamaica
    "+962": "JO",  # Jordan
    "+81": "JP",  # Japan
    "+254": "KE",  # Kenya
    "+996": "KG",  # Kyrgyzstan
    "+855": "KH",  # Cambodia
    "+686": "KI",  # Kiribati
    "+269": "KM",  # Comoros
    "+1-869": "KN",  # Saint Kitts And Nevis
    "+850": "KP",  # Korea, Democratic People's Republic Of
    "+82": "KR",  # Korea, Republic of
    "+965": "KW",  # Kuwait
    "+1-345": "KY",  # Cayman Islands
    "+7": "KZ",  # Kazakhstan
    "+856": "LA",  # Lao People's Democratic Republic
    "+961": "LB",  # Lebanon
    "+1-758": "LC",  # Saint Lucia
    "+423": "LI",  # Liechtenstein
    "+94": "LK",  # Sri Lanka
    "+231": "LR",  # Liberia
    "+266": "LS",  # Lesotho
    "+370": "LT",  # Lithuania
    "+352": "LU",  # Luxembourg
    "+371": "LV",  # Latvia
    "+218": "LY",  # Libya
    "+212": "MA",  # Morocco
    "+377": "MC",  # Monaco
    "+373": "MD",  # Moldova, Republic of
    "+382": "ME",  # Montenegro
    "+590": "MF",  # Saint Martin
    "+261": "MG",  # Madagascar
    "+692": "MH",  # Marshall Islands
    "+389": "MK",  # Macedonia, the Former Yugoslav Republic Of
    "+223": "ML",  # Mali
    "+95": "MM",  # Myanmar
    "+976": "MN",  # Mongolia
    "+853": "MO",  # Macao
    "+1-670": "MP",  # Northern Mariana Islands
    "+596": "MQ",  # Martinique
    "+222": "MR",  # Mauritania
    "+1-664": "MS",  # Montserrat
    "+356": "MT",  # Malta
    "+230": "MU",  # Mauritius
    "+960": "MV",  # Maldives
    "+265": "MW",  # Malawi
    "+52": "MX",  # Mexico
    "+60": "MY",  # Malaysia
    "+258": "MZ",  # Mozambique
    "+264": "NA",  # Namibia
    "+687": "NC",  # New Caledonia
    "+1-869": "NE",  # Saint Kitts And Nevis
    "+227": "NE",  # Niger
    "+234": "NG",  # Nigeria
    "+683": "NI",  # Niue
    "+672": "NL",  # Netherlands
    "+47": "NO",  # Norway
    "+977": "NP",  # Nepal
    "+670": "NR",  # Nauru
    "+1-649": "NU",  # Norfolk Island
    "+64": "NZ",  # New Zealand
    "+505": "NI",  # Nicaragua
}


def added_number(*number, **code):
    url = "https://sms.tsupertools.com/livewire/message/backend.numbers.numbers"

    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "text/html, application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://sms.tsupertools.com/admin/numbers",
        "Content-Type": "application/json",
        "X-Livewire": "true",
        "X-Csrf-Token": "KFchXEEc3x9VVCTeJ1E2qdgpa5nDEDV1L5wfyr57",
        "Origin": "https://sms.tsupertools.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
        "Te": "trailers",
    }

    # Cookies
    cookies = {
        "_session": "eyJpdiI6ImNPZndKZE5tWDFGaHQ5Z3FTbno2ekE9PSIsInZhbHVlIjoiYThJZ1IrVHFJR1gxdkM2R0FUb3R4OFBFdFhWeDEzQVRjd0JIb2txWVJ5WVdYWHBqVWwrd1Nic2R5a2lSZ0k3NHl5Z3FTVDV3Q1NmNGpiMEFwUm5XbFFUVVB6djR1S0dwWWg0N0hYaklsbTR5U1hvYXBXbm12cVIwNW1jK0dXSDMiLCJtYWMiOiIxMzYzNWY4ZDZkNmJjOTgyM2I2YmRhYjhmN2YyZDA5YjQ4ZWM2NjRhYzkxODRmZDdiODk1MmRjOWUwMmNjMjc0IiwidGFnIjoiIn0%3D",
        "XSRF-TOKEN": "eyJpdiI6ImZaMGZsV0dCZ2lpaHRLVXJrWlhQbFE9PSIsInZhbHVlIjoiZit2U0hoTE1oWit2eDNUNXoxOVR3dnBTUFJ6QkZoVjFXL2IwZ0VBQjBQdEtmTUVyRTljTW94R3NVbTBGWGE3WVBtR2pGK3lMZGVJSEZQVFdUamI4dzFrQ1lpMlNTY3NzNG1Nb0lCYTJHMGUyQndzeFFMMHY2MXFaQm9YRFRTdS8iLCJtYWMiOiIzOGY0Y2E0YzlmMzYzYTY4OTlmNjQ3NjZmMjAzOGRjNjQzZjJkMzIzMGY1M2RhMDViMmFlYWY2NGUyMmM0YjA0IiwidGFnIjoiIn0%3D",
        "cf_clearance": "1WNV8OEUvTSbeNYr_M625fwG8QKWrQ3Ngfz75RxXwTE-1731516595-1.2.1.1-t9DXOxo97ADE4szDEgtPviq3HMnlebmSGAUMxz9joIHMrsm8.s2PthSL88oHqFOdTfh3e_JGksNC8rBC3m_zg18qtxqaLitzuro.uuWcLozF7dDwczugT0tNzr0MPP4BFaTya9VgXDM.AwREgPjtIsb6vZPbz9AwejzyW83d8Eb7ogINpLodcTnaKI8xU8OOW.PQMDIFINVbwR84Vnh2uCuUynQ74QhElw_9m7EI9CmC3CUFflQIaB4w1AzGherIaAxhuE8yvitAtXZeNDeuqjKo7eSCpwHfk9XExDcCs4plxhmfs.klEP8Dd1JqPl0.TT2kGhV8M7QSs2NZ8kUmkw",
    }

    # JSON payload
    data = {
        "fingerprint": {
            "id": "2auxwIvcwVLjivECnr0e",
            "name": "backend.numbers.numbers",
            "locale": "en",
            "path": "admin/numbers",
            "method": "GET",
            "v": "acj",
        },
        "serverMemo": {
            "children": [],
            "errors": [],
            "htmlHash": "14c90b42",
            "data": {
                "error": None,
                "search": "",
                "order": "asc",
                "orderby": "id",
                "numbers": [],
                "number": {
                    "id": None,
                    "number": "",
                    "country": None,
                    "meta": None,
                    "type": None,
                    "status": 1,
                    "page_title": None,
                    "custom_header": None,
                },
                "numberToAssign": None,
                "assignees": [],
                "showManageAssignees": False,
                "users": [],
                "user": None,
                "types": [
                    "Open",
                    "Register Only",
                    "Private",
                    "Shared Buy",
                    "Private Buy",
                ],
                "filters": {"type": None},
                "bg": [
                    "bg-gray-200",
                    "bg-lime-200",
                    "bg-red-200",
                    "bg-purple-200",
                    "bg-pink-200",
                ],
                "text": [
                    "text-gray-800",
                    "text-lime-800",
                    "text-red-800",
                    "text-purple-800",
                    "text-pink-800",
                ],
            },
            "dataMeta": {
                "modelCollections": {
                    "numbers": {
                        "class": "App\\Models\\Number",
                        "id": [1, 2],
                        "relations": [],
                        "connection": "mysql",
                        "collectionClass": None,
                    },
                    "users": {
                        "class": "App\\Models\\User",
                        "id": [1],
                        "relations": [],
                        "connection": "mysql",
                        "collectionClass": None,
                    },
                }
            },
            "checksum": "150b8107be94fee1b1e8a85da4a81474067c83717414e0049ac84cf3567cd3f9",
        },
        "updates": [
            {
                "type": "syncInput",
                "payload": {"id": "noc3", "name": "number.type", "value": "0"},
            },
            {
                "type": "syncInput",
                "payload": {"id": "qkbt", "name": "number.country", "value": code},
            },
            {
                "type": "syncInput",
                "payload": {
                    "id": "f81u",
                    "name": number,
                    "value": number,
                },
            },
            {
                "type": "callMethod",
                "payload": {"id": "im7u", "method": "handle", "params": []},
            },
        ],
    }

    # Making the POST request
    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    print(response.status_code)


def smstome():
    data = requests.get("https://smstome.com/")
    soup = BeautifulSoup(data.text, "html.parser")

    data = soup.findAll("a", attrs={"class": "button-clear"})

    for country in data:
        link = country["href"]
        numbers = []
        href = []
        data = requests.get("https://smstome.com" + link)
        soup = BeautifulSoup(data.text, "html.parser")

        data = soup.findAll("a", attrs={"class": "numbutton"})

        for x in data:
            # print(x["href"])
            href.append(x["href"])
            numbers.append(x.text)

        for href, phone in zip(href, numbers):
            data = requests.get(href)
            soup = BeautifulSoup(data.text, "html.parser")

            data = soup.findAll("tbody")

            for table_body in data:
                rows = table_body.find_all("tr") if table_body else []

                # Data lists to store scraped information
                numbers = []
                timestamps = []
                messages = []

                # Loop through each row and get data from each <td>
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) >= 3:
                        # Extract phone number, timestamp, and message text
                        number = cells[0].get_text(strip=True)
                        timestamp = cells[1].get_text(strip=True)
                        message = cells[2].get_text(strip=True)

                        # Append to respective lists
                        numbers.append(number)
                        timestamps.append(timestamp)
                        messages.append(message)

                # Print the scraped data
                for num, time, msg in zip(numbers, timestamps, messages):
                    print(f"Number: {phone}")
                    print(f"Timestamp: {time}")
                    print(f"Message: {msg}")
                    print("-" * 40)
                    import time

                    uuid = random.randint(6, 1000000)
                    encmsg = urllib.parse.quote(msg)
                    request = f"https://sms.tsupertools.com/api/receive/ptaoqimhcgwblus9vxk7fdyn86erj?to={phone}&from={phone}&msg={encmsg}&uuid={uuid}"
                    headers = {
                        "Cookie": "cf_clearance=IhAbGrMYfDXLR6m4fcOY9RfUoCZ.Tqcph3goCvzN7mM-1731059587-1.2.1.1-LR2sChBVC6ItqTsk8f8DhleI.DxFdcnDcWlogJlItgqMxMzDm0VGd5kKHfR7jk08zoYKFSrSFBbbPuuylIHMQaNRIXJBlpKJp2unC17s78kZz.pZnfy98I0JpbGMSZvKEN3w3OiG5.jEYEJCDF6JgGo6HxbZhKhYukoe4mL6ki_BG9t1jeLGlOKx2lnXdQbpnBmHLr7QKNiYImCz2sfreuJ86twLkgcnqWRP7yTxTm.NgcWw33KkXJ0fcMoZytXwM82cuwcZoT3DkyOlf0vaxeztJGddF2DgnTrWLr0o9YDF7dDivr7y.iWb3tR68VY5ayHmFHLPgDrsj3.MS8vd1A",
                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Priority": "u=0, i",
                        "Te": "trailers",
                    }

                    req = requests.get(request, headers=headers)
                    match = re.match(r"^\+(\d{1,3})", phone)
                    # if match:
                    #     country_code = "+" + match.group(
                    #         1
                    #     )  # Get the matched country code
                    #     country = country_codes.get(country_code)
                    #     added_number(number.text.replace("+", ""), country)
                    added_number(number.text.replace("+", ""))
                    print(req.status_code)
                    print("-" * 40)
                    # print(req.text)
                    time.sleep(10)


def recivesms():
    headers = {
        "Cookie": "PHPSESSID=g8qbra0mrgrcjsn11cs53qp74i; phps=1731130199; _ga=GA1.1.1430283938.1731130203; _gid=GA1.2.1767883693.1731130203; _ga_LLL30FE8DG=GS1.1.1731133533.2.0.1731133536.57.0.0; __gads=ID=acd9e33b4be9daa5:T=1731130204:RT=1731133532:S=ALNI_MZQuAvS2D0AeJw5WkH9EAU43BdsgA; __gpi=UID=00000f843ee7fa9c:T=1731130204:RT=1731133532:S=ALNI_MaDHYapk4aun0RgcjbN2Kx6UXjnxA; __eoi=ID=19a574f0c9e4f591:T=1731130204:RT=1731133532:S=AA-AfjaCZrbCnp5Oq2n5oJ36-dWd; __gsas=ID=6ee609a448c2dc7e:T=1731130208:RT=1731130208:S=ALNI_MYLj13SQH0ThCWTQzCcDVDwjVbFAg; _gat_gtag_UA_117293263_1=1; FCNEC=%5B%5B%22AKsRol_DNIF5I6zJBXNioSiOR3Cp51nsuSV5U562br5aOg4QeeTIvCyD4ZZGxBlqbr3ZcCtYvLoZClpJwoTBvY1_weHUFqzceV3xobXVTK5uZ7F0b6BCyJwnm54xS2esEhAgV2LnFMCN5EbioyxFobJOa67G1oyQ5g%3D%3D%22%5D%5D",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "Te": "trailers",
    }
    data = requests.get("https://receive-smss.com/", headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")
    getlink = soup.findAll("a", attrs={"class": "number-boxes1-item-button"})
    getnumbers = soup.findAll("div", attrs={"class": "number-boxes-itemm-number"})
    for links, number in zip(getlink, getnumbers):
        links = links["href"]
        links = f"https://receive-smss.com{links}"
        data = requests.get(links, headers=headers)
        soup = BeautifulSoup(data.text, "html.parser")
        getsms = soup.findAll("div", attrs={"class": "list-view"})
        for x in getsms:
            sms = x.find("div", attrs={"class": "msgg"})
            sender = x.find("div", attrs={"class": "senderr"})
            time = x.find("div", attrs={"class": "time"})
            sender = sender.text.replace("Sender", "")
            sms = sms.text.replace("Message", "")
            time = time.text.replace("Time", "")
            print("-" * 40)
            print(f"Number :{number.text}")
            print(f"From :{sender}")
            print(f"sms :{sms}")
            print(f"Time:{time}")
            print("-" * 40)
            import time

            uuid = random.randint(6, 1000000)
            encmsg = urllib.parse.quote(sms)
            request = f"https://sms.tsupertools.com/api/receive/ptaoqimhcgwblus9vxk7fdyn86erj?to={number.text}&from={sender}&msg={encmsg}&uuid={uuid}"
            print(request)
            headers = {
                "Cookie": "cf_clearance=IhAbGrMYfDXLR6m4fcOY9RfUoCZ.Tqcph3goCvzN7mM-1731059587-1.2.1.1-LR2sChBVC6ItqTsk8f8DhleI.DxFdcnDcWlogJlItgqMxMzDm0VGd5kKHfR7jk08zoYKFSrSFBbbPuuylIHMQaNRIXJBlpKJp2unC17s78kZz.pZnfy98I0JpbGMSZvKEN3w3OiG5.jEYEJCDF6JgGo6HxbZhKhYukoe4mL6ki_BG9t1jeLGlOKx2lnXdQbpnBmHLr7QKNiYImCz2sfreuJ86twLkgcnqWRP7yTxTm.NgcWw33KkXJ0fcMoZytXwM82cuwcZoT3DkyOlf0vaxeztJGddF2DgnTrWLr0o9YDF7dDivr7y.iWb3tR68VY5ayHmFHLPgDrsj3.MS8vd1A",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Priority": "u=0, i",
                "Te": "trailers",
            }

            req = requests.get(request, headers=headers)
            print(req.status_code)
            print("-" * 40)
            # match = re.match(r"^\+(\d{1,3})", number.text)
            # if match:
            #     country_code = "+" + match.group(1)  # Get the matched country code
            #     country = country_codes.get(country_code)
            #     added_number(number.text.replace("+", ""), country)
            # # print(req.text)
            added_number(number.text.replace("+", ""))
            time.sleep(10)


threading.Thread(target=recivesms).start()
threading.Thread(target=smstome).start()

# key_lengths = {len(key) for key in country_codes}
# print(key_lengths)
# match = re.match(r"^\+(\d{1,1})", "+97598328055")
# if match:
#     country_code = "+" + match.group(1)  # Get the matched country code
#     country = country_codes.get(country_code)
#     print(country)
