import scraping_resin as sr

state_url = "https://weedmaps.com/listings/in/united-states/new-york"
city_href_list = sr.get_city_hrefs(state_url)

for city_href in city_href_list:
    city_url = f"https://weedmaps.com{city_href}"
    print(city_url)
    dispensary_hrefs = sr.get_dispensary_hrefs(city_url)
    all_data = [sr.scrape_data_from_href(dispensary_href) for dispensary_href in dispensary_hrefs]
    sr.data_to_csv(all_data, "new_york_state.csv")
