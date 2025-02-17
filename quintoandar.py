import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suacasa.settings')
django.setup()

from home.models import Property

import requests
import csv

from bs4 import BeautifulSoup
import json

import math
import random
import string

def generate_random_string(length=32):
    """Gera uma string aleatória com o comprimento especificado."""
    characters = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    return ''.join(random.choices(characters, k=length))


def get_neighborhoods(citie_id):
    url = "https://www.quintoandar.com.br/city/{citie_id}?neighborhoodBusinessContext=RENT".format(
        citie_id=citie_id)
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    json_data = response.json()
    neighbourhoods = json_data["neighborhoods"]
    data = []
    for neighbourhood in neighbourhoods:
        data.append({
            "id": neighbourhood["id"],
            "name": neighbourhood["name"],
            "slug": neighbourhood["slug"],
        })
    return data


def get_cities(): 
    url = "https://www.quintoandar.com.br/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar o elemento "__NEXT_DATA__"
    json_text = soup.find("script", {"id": "__NEXT_DATA__"}).text
    json_data = json.loads(json_text)
    cities = json_data["props"]["pageProps"]["cities"]
    data = []
    import ipdb; ipdb.set_trace();
    for citie in cities:
        region_id = citie['regionId']
        neighborhoods = get_neighborhoods(region_id)
        print(citie["name"], len(neighborhoods))
        data.append({
            "id": citie["placeId"],
            "name": citie["name"],
            "slug": citie["slug"],
            "stateName": citie["stateName"],
            "stateShortName": citie["stateShortName"],
            "neighborhoods": neighborhoods,
        })

    return data


def get_payload(citie_slug, type, page_size=1, offset=0):

    return {
        "context": {
            "mapShowing": False,
            "listShowing": True,
            "userId": "WulzPncPrBR4z1Nf9FaxnlCE55vnTOaoiqDnsBhJg_J4ZTaAh9_7rA",
            "deviceId": "WulzPncPrBR4z1Nf9FaxnlCE55vnTOaoiqDnsBhJg_J4ZTaAh9_7rA",
            "searchId": generate_random_string(),
            "numPhotos": 12,
            "isSSR": False
        },
        "filters": {
            "businessContext": type,
            "blocklist": [],
            "selectedHouses": [],
            "location": {
                "coordinate": {},
                "viewport": {},
                "neighborhoods": [],
                "countryCode": "BR"
            },
            "priceRange": [],
            "specialConditions": [],
            "excludedSpecialConditions": [],
            "houseSpecs": {
                "area": {
                    "range": {}
                },
                "houseTypes": [],
                "amenities": [],
                "installations": [],
                "bathrooms": {
                    "range": {}
                },
                "bedrooms": {
                    "range": {}
                },
                "parkingSpace": {
                    "range": {}
                },
                "suites": {
                    "range": {}
                }
            },
            "availability": "ANY",
            "occupancy": "ANY",
            "partnerIds": [],
            "categories": []
        },
        "sorting": {
            "criteria": "RELEVANCE",
            "order": "DESC"
        },
        "pagination": {
            "pageSize": page_size,
            "offset": offset
        },
        "slug": citie_slug,
        "fields": [
            "id",
            "coverImage",
            "rent",
            "totalCost",
            "salePrice",
            "iptuPlusCondominium",
            "area",
            "imageList",
            "imageCaptionList",
            "address",
            "regionName",
            "city",
            "visitStatus",
            "activeSpecialConditions",
            "type",
            "forRent",
            "forSale",
            "isPrimaryMarket",
            "bedrooms",
            "parkingSpaces",
            "suites",
            "listingTags",
            "yield",
            "yieldStrategy",
            "neighbourhood",
            "categories",
            "bathrooms",
            "isFurnished",
            "installations",
            "amenities",
            "shortRentDescription",
            "shortSaleDescription"
        ],
        "locationDescriptions": [
            {
                "description": citie_slug
            }
        ]
    }


def do_request(slug, type):

    payload = get_payload(slug, type)

    url = "https://apigw.prod.quintoandar.com.br/house-listing-search/v2/search/list"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    data = []
    

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_as_a_json = response.json()
        total_rents_to_search = response_as_a_json["hits"]["total"]["value"]
        data.extend(response_as_a_json['hits']['hits'])

        page_size = 1000
        max_pages = math.ceil(total_rents_to_search / page_size)

        for page in range(max_pages):
            offset = page * page_size
            print(f"Buscando página {page + 1}...")
            payload = get_payload(slug, type, page_size, offset)
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                    response_as_a_json = response.json()
                    data.extend(response_as_a_json['hits']['hits'])
                    print("total já add: {}".format(len(data)))
        return data

def get_all():
    cities = get_cities()
    for citie in cities:
        neighbourhoods = citie["neighborhoods"]
        for neighbourhood in neighbourhoods:
            slug = neighbourhood["slug"]
            print(slug)
            hits = do_request(slug, "RENT")
            if hits: 
                data = []
                for hit in hits:
                    id = hit['_id']
                    source = hit['_source']
                    type = source.get("type")
                    area = source.get("area")
                    bathrooms = source.get("bathrooms")
                    bedrooms = source.get("bedrooms")
                    suites = source.get("suites")
                    parkingSpaces = source.get("parkingSpaces")
                    amenities = source.get("amenities")
                    if amenities: 
                        amenities = ", ".join(amenities)
                    installations = source.get("installations")
                    if installations:
                        installations = ", ".join(installations)
                    coverImage = source.get("coverImage")
                    salePrice = source.get("salePrice")
                    iptuPlusCondominium = source.get("iptuPlusCondominium")
                    direct_url = "{prefix}/{id}/comprar/".format(
                        prefix="https://www.quintoandar.com.br/imovel/",
                        id=id
                    )
                    orderedImageList = hit["orderedImageList"]
                    forRent = source.get("forRent")
                    forSale = source.get("forSale")
                    rent_price = source.get("rent")
                    total_cost_rent = source.get("totalCost")
                    address = source.get("address")
                    city = source.get("city")
                    neighbourhood = source.get("neighbourhood")
                    regionName = source.get("regionName")

                    try:
                        Property.objects.get(uu_id=id)
                    except Property.DoesNotExist:
                        Property.objects.create(
                            uu_id=id,
                            type=type,
                            area=area,
                            bathrooms=bathrooms,
                            bedrooms=bedrooms,
                            suites=suites,
                            parkingSpaces=parkingSpaces,
                            amenities=amenities,
                            installations=installations,
                            salePrice=salePrice,
                            iptuPlusCondominium=iptuPlusCondominium,
                            url_coverImage=coverImage,
                            url_orderedImageList=orderedImageList,
                            direct_url=direct_url,
                            forRent=forRent,
                            forSale=forSale,
                            rent_price=rent_price,
                            total_cost_rent=total_cost_rent,
                            source="quintoandar",
                            address=address,
                            city=city,
                            neighbourhood=neighbourhood,
                            regionName=regionName,
                        )

get_all()