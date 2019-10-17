from bs4 import BeautifulSoup
import requests
import csv
import os

def get_city_hrefs(state_url):
    r = requests.get(state_url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    city_elements = soup.find_all("a", {"data-testid": "region-link"})
    city_hrefs = [city_element["href"] for city_element in city_elements]

    return city_hrefs


# get the hrefs to all individual dispensary pages
def get_dispensary_hrefs(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    dispensary_element_class = "map-listings-list__ListItem-sc-1ynfzzj-1 bVQzPb"
    dispensary_elements = soup.find_all("div", {"class": dispensary_element_class})
    dispensary_hrefs = [dispensary_element.a['href'] for dispensary_element in dispensary_elements]

    return dispensary_hrefs


# scrape all relevant info from a given href
def scrape_data_from_href(href):
    r = requests.get(f"https://weedmaps.com{href}/about")
    if r.status_code == 404:
        r = requests.get(f"https://weedmaps.com{href}")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    dispensary_data = {}
    dispensary_data["name"] = soup.find("h1", {"data-test-id": "listing-name"}).text
    dispensary_data["phone_number"] = soup.find("div", {"display": "none,none,none,block,block"}).text
    unshortened_location = soup.find("span", {"data-test-id": "listing-type"}).text
    location_start_index = unshortened_location.find("•")
    dispensary_data["location"] = unshortened_location[location_start_index + 2:]
    dispensary_data["type_of_listing"] = unshortened_location[:location_start_index - 1]
    dispensary_data["email"] = soup.find("div",
                                         {"class": "src__Box-sc-1sbtrzs-0 styled-components__DetailGridItem-d53rlt-0 "
                                                   "styled-components__Email-d53rlt-3 icSxPE"}).a.text
    if dispensary_data["email"] == "customerservice@weedmaps.com" or dispensary_data["email"] == "test@test.com":
        dispensary_data["email"] = None

    try:
        dispensary_data["website"] = soup.find("div", {"class": "src__Box-sc-1sbtrzs-0 "
                                                                "styled-components__DetailGridItem-d53rlt-0 "
                                                                "styled-components__Website-d53rlt-4 uWbmk"}).a.text
    except AttributeError:
        dispensary_data["website"] = None

    return dispensary_data


def data_to_csv(all_data, csv_filename):
    csv_columns = ["name", "type_of_listing", "phone_number", "location", "email", "website"]
    try:
        file_exists = os.path.isfile(csv_filename)
        with open(csv_filename, "a", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, csv_columns)
            if not file_exists:
                writer.writeheader()
            for data in all_data:
                writer.writerow(data)
    except IOError:
        print("IOError")
