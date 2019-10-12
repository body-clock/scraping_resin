from bs4 import BeautifulSoup
import requests
import csv


def get_dispensary_hrefs(url, div_class):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    dispensary_elements = soup.find_all("div", {"class": div_class})
    dispensary_hrefs = [dispensary_element.a['href'] for dispensary_element in dispensary_elements]

    return dispensary_hrefs


def scrape_data_from_href(href):
    r = requests.get(f"https://weedmaps.com{href}/about")
    if r.status_code == 404:
        r = requests.get(f"https://weedmaps.com{href}")
    print(r.url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    dispensary_data = {}
    dispensary_data["name"] = soup.find("h1", {"data-test-id": "listing-name"}).text
    dispensary_data["phone_number"] = soup.find("div", {"display": "none,none,none,block,block"}).text
    unshortened_location = soup.find("span", {"data-test-id": "listing-type"}).text
    location_start_index = unshortened_location.find("•") + 2
    dispensary_data["location"] = unshortened_location[location_start_index:]
    dispensary_data["email"] = soup.find("div",
                                         {"class": "src__Box-sc-1sbtrzs-0 styled-components__DetailGridItem-d53rlt-0 "
                                                   "styled-components__Email-d53rlt-3 icSxPE"}).a.text
    if dispensary_data["email"] == "customerservice@weedmaps.com":
        dispensary_data["email"] = None

    try:
        dispensary_data["website"] = soup.find("div", {"class": "src__Box-sc-1sbtrzs-0 "
                                                                "styled-components__DetailGridItem-d53rlt-0 "
                                                                "styled-components__Website-d53rlt-4 uWbmk"}).a.text
    except AttributeError:
        dispensary_data["website"] = None

    return dispensary_data

def data_to_csv(all_data):
    csv_columns = ["name", "phone_number", "location", "email", "website"]
    csv_file = "newyork_data.csv"
    try:
        with open(csv_file, "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, csv_columns)
            writer.writeheader()
            for data in all_data:
                writer.writerow(data)
    except IOError:
        print("IOError")



scraping_url = "https://weedmaps.com/listings/in/united-states/new-york/manhattan"
scraping_class = "map-listings-list__ListItem-sc-1ynfzzj-1 bVQzPb"
hrefs = get_dispensary_hrefs(scraping_url, scraping_class)
all_data = [scrape_data_from_href(href) for href in hrefs]
test_data = [scrape_data_from_href(href) for href in hrefs]
data_to_csv(all_data)
