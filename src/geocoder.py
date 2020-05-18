
from mapbox import Geocoder

import json
import urllib
import time
from random import gauss
import logging as logger
logger.basicConfig(level=logger.ERROR)

import os
import sys

def fetch_data(
    path="https://api.covid19india.org/resources/resources.json", geojson=False
):
    request = urllib.request.urlopen(path)
    data = json.load(request)
    if geojson:
        return data

    inputDict = data["resources"]
    return inputDict


def save_data(save_this, fname="output"):
    with open("./tmp/resources/" + fname + ".json", "w") as json_file:
        json.dump(save_this, json_file, indent=4)


class EssentialsConverter:
    def __init__(self):
        # Public API. So commiting with code. No big secret here.

#         self.access_token = "pk.eyJ1IjoiYXNobWFwNGdkIiwiYSI6ImNrOXBjb2k2dDA5YW4zb24xb3A2cWs5YXYifQ.3qtCEWPKAOEftYEEUDfDSQ"
        self.access_token = "pk.eyJ1IjoiYXNocm9uYXZvbmEiLCJhIjoiY2thYjRtY2hmMDkyeDJ0bzg0cHF5dTh5diJ9.10oEwG3nFpYrhYy-LufSuA"
        self.coder = Geocoder(access_token=self.access_token)
        self.cityDict = {}
        self.cityList = []
        self.processedBatch = []
        self.failed = []
        self.failed_ids = []
        self.failed_cities = []
        self.gaussian = []
        self._api = 0

    @property
    def request_ctr(self):
        self._api += 1

    @property
    def rate_limit_exceeded(self):
        return self._api and not self._api % 600

    def populate_cities(self, dir="./tmp/resources/", fromFile=False):
        if fromFile:
            try: 
                with open(dir + "cityData.json") as c_list:
                    data = json.load(c_list)
            except FileNotFoundError:
                logger.error('Wanted to access cityData, but not found')
                pass

            self.cityDict = data["cityboundaries"]
            self.cityList = data["cities"]
        else:  # read in city list and city dicts from other sources like the google sheet
            logger.warning('CityData file not used')
            pass

    def generate_geojson(self, oldData=None):
        update = []
        if oldData:
            update = oldData["features"]
        update += self.processedBatch

        geojson = {
            "type": "FeatureCollection",
            "lastupdated": time.ctime(),
            "features": update,
        }

        return geojson
    def check_city(self, entry):
        city = " ".join((entry["city"], entry["state"]))

        if city not in self.cityList:
            self.make_boundaries(city)
            self.cityList.append(city)

    def make_boundaries(self, city):
        lvl1 = ["district"]
        lvl2 = ["place"]
        lvl3 = ["place", "locality", "neighborhood"]

        self.request_ctr
        response = self.coder.forward(city, types=lvl1, country=["in"], limit=1)

        if not response.json()["features"]:
            self.request_ctr
            response = self.coder.forward(city, types=lvl2, country=["in"], limit=1)

            # if not response.json()["features"]:
            #     self.request_ctr
            #     response = self.coder.forward(city, types=lvl2, country=["in"], limit=1)

            if not response.json()["features"]:
                self.request_ctr
                response = self.coder.forward(
                    city, types=lvl3, country=["in"], limit=1
                )

                if not response.json()["features"]:
                    self.request_ctr
                    response = self.coder.forward(city, country=["in"], limit=1)

        if not response.json()["features"]:
            self.failed_cities.append(city)
            return

        feat = response.json()["features"][0]
        city_center = feat["center"]

        if "bbox" in feat.keys():
            city_bbox = feat["bbox"]
        else:
            city_bbox = []

        self.cityDict[city] = {"bbox": city_bbox, "center": city_center}

        logger.info(f"Boundaries for {city} has been added successfully")

    @staticmethod
    def get_icon(category):
        if category == "Accommodation and Shelter Homes":
            return "homes"
        elif category == "Ambulance":
            return "ambulance"
        elif category == "Community Kitchen":
            return "kitchen"
        elif category == "CoVID-19 Testing Lab":
            return "lab"
        elif category == "Delivery [Vegetables, Fruits, Groceries, Medicines, etc.]":
            return "delivery"
        elif category == "Fire Brigade":
            return "fire"
        elif category == "Free Food":
            return "food"
        elif category == "Fundraisers":
            return "fund"
        elif category == "Government Helpline":
            return "helpline"
        elif category == "Hospitals and Centers":
            return "hospital"
        elif category == "Mental well being and Emotional Support":
            return "wellbeing"
        elif category == "Police":
            return "police"
        elif category == "Senior Citizen Support":
            return "seniors"
        elif category == "Transportation":
            return "transport"
        elif category == "Quarantine Facility":
            return "quarantine"
        elif category == "Other":
            return "other"

        else:
            return "unknown"

    @staticmethod
    def scrape_url(url, start=33, end=None):
        reg = url[start:end].split(",")

        geom = {"type": "Point", "coordinates": [reg[1], reg[0]]}
        return geom

    def make_feature(self, entry):
        url_format = "http://www.google.com/maps/place/"

        # Parse entry data
        i = entry["recordid"]
        name = entry["nameoftheorganisation"]
        desc = entry["descriptionandorserviceprovided"]
        category = entry["category"]
        state = entry["state"]
        phone = entry["phonenumber"]
        contact = entry["contact"]

        # Declare new props
        q_name = ""
        q_addr = ""
        geom = {}

        # Set flags
        icon = self.get_icon(entry["category"])
        isHealthcare = 0

        if category == "CoVID-19 Testing Lab" or category == "Hospitals and Centers":
            isHealthcare = 1

        city = " ".join((entry["city"], entry["state"]))
        query = ", ".join((entry["nameoftheorganisation"], entry["city"]))

        maps = False
        if url_format in contact:
            maps = True


        if "PAN" in city:
            if "India" in city:
                query = "India"
                state = "PAN India"
            else:
                query = entry["city"]
                state = " ".join(["PAN", state])
                logger.info("Pan entry saved as ", state)

        
        # Skipped entries

        if city not in self.cityDict:
            self.failed.append(entry)
            self.failed_ids.append(i)
            return

        c_bbox = self.cityDict[city]["bbox"]
        c_center = self.cityDict[city]["center"]


        if not maps:
            if c_bbox != []:
                self.request_ctr
                resp = self.coder.forward(query, country=["in"], bbox=c_bbox, limit=1)
            else:
                self.request_ctr
                resp = self.coder.forward(query, country=["in"], limit=1)

            target = resp.geojson()

            # Get data
            if target["features"]:  # condition -> non empty response
                geom = target["features"][0]["geometry"]
                q_name = target["features"][0]["text"]
                q_addr = target["features"][0]["place_name"]
            else:  # else -> empty response - use big brain trickery
                self.gaussian.append(i)
                if c_bbox:
                    sd = min(abs(c_bbox[0] - c_bbox[2]) / 8, abs(c_bbox[1] - c_bbox[3]) / 8)
                else:
                    sd = c_center[0] * 0.0004

                lng = gauss(c_center[0], sd)
                lat = gauss(c_center[1], sd)

                geom = {"type": "Point", "coordinates": [lng, lat]}
                q_addr = city
                q_name = ""
        
            
        if url_format in contact:
            geom = self.scrape_url(contact)
            self.request_ctr
            reverse = self.coder.reverse(geom["coordinates"][0], geom["coordinates"][1])
            target = reverse.geojson()

            if target["features"]:
                q_name = target["features"][0]["text"]
                q_addr = target["features"][0]["place_name"]

        if "PAN" in city:
            if "India" in city:
                q_addr = "India"
            else:
                q_addr = ", ".join([entry["state"], "India"])

        prop = {
            "recordid": i,
            "name": name,
            "desc": desc,
            "geoTag": q_name,
            "addr": q_addr,
            "state": state,
            "phone": phone,
            "contact": contact,
            "priority": isHealthcare,
            "icon": icon,
        }

        self.processedBatch.append(
            {"type": "Feature", "properties": prop, "geometry": geom}
        )

    def process_entry(self, entry):
        self.check_city(entry)  # Generates city data if its not been done yet.
        self.make_feature(entry)
        logger.info(f'Processed #{entry["recordid"]}')


def main():
    # Get the latest resources.json
    # entries = fetch_data()

    converter = EssentialsConverter()

    print('Geocoding begins')

    """Read the recently fetched resources.json copied to tmp folder"""
    with open("./tmp/resources/resources.json") as f:
        entries = json.load(f)["resources"]

    """Read in old geojson via url or filepath"""
    # old_entries = fetch_data(path="https://raw.githubusercontent.com/aswaathb/covid19india-react/publish/newResources/geoResources.json", geojson=True)
    processed_i = []  # cache recordid's for previously processed features
    try:
        
        with open("./tmp/resources/geoResources.json") as geo:
            old_entries = json.load(geo)

        for feature in old_entries["features"]:
            processed_i.append(int(feature["properties"]["recordid"]))

        # Load saved city boundaries
        converter.populate_cities(fromFile=True)
        
        for idx, entry in enumerate(entries):
            if int(entry["recordid"]) not in processed_i:
                # convert only the missing entries
                converter.process_entry(entry)

                if converter.rate_limit_exceeded:
                    logger.info("API rate limit: Minute delay could be added")
                    time.sleep(20)

        # Feed in processed_entries as oldData to append new batch to previously geocoded entries
        feature_collection = converter.generate_geojson(
            oldData=old_entries
        )

    except FileNotFoundError:
        logger.warning("Prefetched file not found. All entries will be geocoded.")
        for idx, entry in enumerate(entries):
            converter.process_entry(entry)
            
            if converter.rate_limit_exceeded:
                logger.info("API rate limit: Minute delay could be added")
                time.sleep(20)

        # Feed in processed_entries as oldData to append new batch to previously geocoded entries
        feature_collection = converter.generate_geojson(
            oldData=None
        ) 

    except Exception as e:
        logger.error('Something went wrong ',e)
        sys.exit("geoResources.json couldn't compare")

    debug = {
        "gaussian": converter.gaussian,
        "failed_cities": converter.failed_cities,
        "failed_ids": converter.failed_ids,
        "failed_entries": converter.failed,
    }

    city_data = {"cities": converter.cityList, "cityboundaries": converter.cityDict}

    save_data(feature_collection, "geoResources")
    save_data(debug, "debug")
    save_data(city_data, "cityData")

    print(f'{len(converter.processedBatch)} records were processed.\n{converter._api} api calls were made')

if __name__ == "__main__":
    main()
