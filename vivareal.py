import os
import django
import django_rq
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suacasa.settings')
django.setup()

from home.models import Property

import math
import cloudscraper
import random
import string


class VivaRealApiClient:

    def __init__(self):
        characters = string.ascii_letters + string.digits 
        device_id = ''.join(random.choices(characters, k=32))
        self.include_field = 'search%28result%28listings%28listing%28contractType%2ClistingsCount%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%2CenhancedDevelopment%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Ctier%29%2Cmedias%2CaccountLink%2Clink%29%29%2CtotalCount%29%2Cpage%2Cfacets%2CfullUriFragments%2Cnearby%28search%28result%28listings%28listing%28contractType%2ClistingsCount%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%2CenhancedDevelopment%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Ctier%29%2Cmedias%2CaccountLink%2Clink%29%29%2CtotalCount%29%29%2Cexpansion%28search%28result%28listings%28listing%28contractType%2ClistingsCount%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%2CenhancedDevelopment%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Ctier%29%2Cmedias%2CaccountLink%2Clink%29%29%2CtotalCount%29%29%2Cdevelopments%28search%28result%28listings%28listing%28contractType%2ClistingsCount%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%2CenhancedDevelopment%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Ctier%29%2Cmedias%2CaccountLink%2Clink%29%29%2CtotalCount%29%29'
        self.user = '8d5d09d9-eb7e-477d-8a16-14afc5f8e908'
        self.category_page = 'RESULT'
        self.page = 1
        self.from_page = 30
        self.business = "SALE"
        self.parentId = "null"
        self.listingType= "USED"
        self.addressLocationId = "BR>Minas Gerais"
        self.addressState = "Minas Gerais"
        self.addressType= "state"
        self.size= "15"
        self.developmentsSize= "0"
        self.images= "webp"
        self.__zt = "mtc:deduplication2023"

        
        self.url = (
            "https://glue-api.vivareal.com/v2/listings?user={user}"
            "&portal=VIVAREAL"
            "&includeFields={include_field}"
            "&categoryPage=RESULT"
            "&page={page}"
            "&from={from_page}"
            "&business=SALE"
            "&parentId=null"
            "&listingType=USED"
            "&addressLocationId=BR%3ERio+de+Janeiro"
            "&addressState=Rio+de+Janeiro"
            "&addressType=state"
            "&size={size}"
            "&developmentsSize=2"
            "&images=webp"
            "&__zt=mtc%3Adeduplication2023"
        )

        self.headers = {
            'Host': 'glue-api.vivareal.com',
            'accept': '*/*,',
            'accept-encoding': 'gzip, deflate, br, zstd,',
            'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,',
            'origin': 'https://www.vivareal.com.br,',
            'priority': 'u=1, i,',
            'referer': 'https://www.vivareal.com.br/,',
            'sec-ch-ua': '\'Not A(Brand;v=8, Chromium;v=132, Google Chrome;v=132\',',
            'sec-ch-ua-mobile': '?0,',
            'sec-ch-ua-platform': 'macOS,',
            'sec-fetch-dest': 'empty,',
            'sec-fetch-mode': 'cors,',
            'sec-fetch-site': 'cross-site,',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36,',
            'x-deviceid': device_id,
            'x-domain': '.vivareal.com.br',
            'Cookie': 'jr1hgjafshsaf0'
        }

    def get_data(self, endpoint):
        scraper = cloudscraper.create_scraper()  
        response = scraper.get(endpoint, headers=self.headers)
        if response.status_code == 200:
            return response.json()
            # return self.parse_data(response.json())
        else:
            return {"error": f"Request failed with status code {response.status_code}"}

    def parse_data(self, total_properties):
        extracted_data = []
        obj_properties = []
        page_size = 100
        max_pages = math.ceil(total_properties / page_size)
        # max_pages = 3
        for page in range(max_pages):
            offset = page * page_size
            print(f"Buscando página {page + 1}...")
            url = self.url.format(
                user=self.user, include_field=self.include_field, 
                page=page, from_page=offset, size=page_size)
            
            data = self.get_data(url)
            listings = data.get("search", {}).get("result", {}).get("listings", [])
            print(len(listings))

            for item in listings:
                listing = item.get("listing")
                id = listing.get("id")
                address = listing.get("address", {})
                amenities = listing.get("amenities", [])
                if amenities:
                    amenities = ", ".join(amenities)
                pricing_infos = listing.get("pricingInfos", [])
                iptuPlusCondominium = 0
                price = 0.0
                if pricing_infos:
                    iptu = pricing_infos[0].get("yearlyIptu", 0)
                    condo_fee = pricing_infos[0].get("monthlyCondoFee", 0)
                    price = pricing_infos[0].get("price", 0)
                    condo_fee_month = 0
                    if condo_fee > 0:
                        condo_fee_month = (condo_fee / 12)
                    iptu_month = 0
                    if iptu > 0:
                        iptu_month = (iptu/12)
                    iptuPlusCondominium = iptu_month + condo_fee_month

                medias = item.get("medias", [])
                media_data = []
                for media in medias:
                    name = media['url'].format(
                            action="crop", width=870, height=707, description=media['id'])
                    media_data.append({
                        "name": name,
                        "caption": media["type"]
                    })


                url = "https://www.vivareal.com.br{}".format(item.get("link")["href"])

                Property.objects.create(
                    uu_id=listing.get("id"),
                    #description=listing.get("description"),
                    #title=listing.get("title"),
                    type=listing.get("type"),
                    area=listing.get("totalAreas")[0] if listing.get("totalAreas") else 0,
                    bathrooms=listing.get("bathrooms")[0] if listing.get("bathrooms") else 0,
                    bedrooms=listing.get("bedrooms")[0] if listing.get("bedrooms") else 0,
                    suites=listing.get("suites")[0] if listing.get("suites") else 0,
                    parkingSpaces=listing.get("parkingSpaces")[0] if listing.get("parkingSpaces") else 0,
                    amenities=amenities,
                    installations=listing.get("installations", []),
                    salePrice=price,
                    iptuPlusCondominium=iptuPlusCondominium,
                    url_coverImage=listing.get("images", {}).get("cover"),
                    url_orderedImageList=media_data,
                    direct_url=url,
                    forRent=listing.get("pricing", {}).get("forRent"),
                    forSale=True,
                    rent_price=listing.get("pricing", {}).get("rentPrice"),
                    total_cost_rent=listing.get("pricing", {}).get("totalCostRent"),
                    source="vivareal",

                    address='{} {}'.format(address.get("street"), address.get("streetNumber")),
                    city=address.get("city"),
                    neighbourhood=address.get("neighborhood"),
                )
                   

            # Property.objects.bulk_create(extracted_data)
            time.sleep(random.uniform(5, 15))
        return extracted_data
            
    def get_total_properties(self):
        url = self.url.format(
            user=self.user, include_field=self.include_field, 
            page=1, from_page=15, size=15)
        data = self.get_data(url)

        total_properties = data.get("search")["totalCount"]
        return total_properties


api_client = VivaRealApiClient()
total_properties = api_client.get_total_properties()
print("Total: ", total_properties)
api_client.parse_data(total_properties)
# data = api_client.get_data(api_client.url)
# parsed_data = api_client.parse_data(data)