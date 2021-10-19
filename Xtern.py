import googlemaps
import pandas as pd
import time
from pandas.core.indexes import category
import plotly.express as px
from eventbrite import Eventbrite
from predicthq import Client
import requests
import json
import reverse_geocoder as rg
import shutil
from os.path import exists

API_kEY = "AIzaSyCNZHlKIkhqcNsjyTGakgrB9V_W_TRwy10"
Token = '1dUmazWnjbONl6CMQ7o5pGkEHMqVb2T_KKFKAYyj'

def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    address = result[0]['name'] + ", " + result[0]['admin1']+ ", " + result[0]['admin2']+ " " + result[0]['cc']  +"."
    return address
    
def get_info(Location,miles,type):    
    gmaps = googlemaps.Client(key=API_kEY)
    geocode_result = gmaps.geocode(Location)
    co_ordinates = geocode_result[0]['geometry']['location']
    search_string = type
    n = 1609.34
    distance = miles * n
    restaurant_list = []
    response = gmaps.places_nearby(location = co_ordinates,keyword = search_string, radius = distance )
    restaurant_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')
    while next_page_token:
        time.sleep(2)
        response = gmaps.places_nearby(location = co_ordinates,keyword = search_string, radius = distance, page_token = next_page_token)
        restaurant_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')
    restaurant_df = pd.DataFrame(restaurant_list)
    new = restaurant_df.filter(['business_status','name','price_level','rating','user_ratings_total'], axis = 1)
    new = new[new['business_status'] == 'OPERATIONAL']
    new.sort_values("name", inplace = True)
    new.drop_duplicates(subset ="name",keep = 'first', inplace = True)
    file_name = Location + "_" + type+".xlsx"
    destination = "Location Details"
    Path = "Location Details/" + file_name
    if exists(Path) == False:
        new.to_excel(file_name)
        shutil.move(file_name, destination)
    return new

def analyze(df):
    Addresses = df['Address']
    info = {}
    things = ["sport","concert","arts","festivals","expos","conference","restaurants"]
    for i in range(len(Addresses)):
        if i >= 1:
            data = {}
            data_ratings = {}
            for j in things:
                x = get_info(Addresses[i],15,j)
                middle = x['rating'].mean()
                data_ratings.update({"Average " + j + " ratings": round(middle,2)})
            info.update({Addresses[i]:data_ratings})
    new = pd.DataFrame.from_dict(info)
    new.to_excel("output.xlsx")

def interactive_visualizations(data_frame):
    points = []
    names = list(data_frame.columns)
    names = names[1:]
    highest = 0
    max = 0
    for i in range(len(names)):
        x = data_frame[names[i]].mean()
        if x > max:
            max = x
            highest = i
        points.append(round(x,2))
    data = {"Names":names, "Average Ratings for events":points}
    fig = px.bar(data, x = "Names", y = "Average Ratings for events", title = "Average ratings of events in the Location", color = "Average Ratings for events")
    fig.write_html("analysis.html")
    fig.show()
    return names[highest]

def top_ten(data_frame,total_ratings):
    df_filtered = data_frame[data_frame['user_ratings_total'] >= total_ratings]
    df = df_filtered.sort_values(by=['rating'], ascending=False)
    df = df.head(10)
    return df

def Event(Address):
    gmaps = googlemaps.Client(key=API_kEY)
    geocode_result = gmaps.geocode(Address)[0]['geometry']['location']
    lat = geocode_result['lat']
    lon = geocode_result['lng']
    location = str(lat) + ',' + str(lon)
    phq = Client(access_token=Token)    
    sport = ""
    concert = ""
    arts = ""
    conference = ""
    expos = ""
    festivals = ""
    for event in phq.events.search( start_around={'origin': '2021-10-23'},end_around={'origin':'2021-10-30'}, within='10km@'+location, category='sports', limit = 1):
        text = event.title + " "+str(event.start) + reverseGeocode(event.location) + "Category: " + event.category
        sport += text
    for event in phq.events.search( start_around={'origin': '2021-11-06'},end_around={'origin':'2021-11-13'}, within='10km@'+location, category='concerts', limit = 1):
        text = event.title + " "+str(event.start) + reverseGeocode(event.location) + "Category: " + event.category
        concert += text
    for event in phq.events.search( start_around={'origin': '2021-11-20'},end_around={'origin':'2021-11-27'}, within='10km@'+location, category='performing-arts', limit = 1):
        text = event.title + " "+str(event.start) + reverseGeocode(event.location) + "Category: " + event.category
        arts += text
    for event in phq.events.search( start_around={'origin': '2021-10-04'},end_around={'origin':'2021-12-31'}, within='10km@'+location, category='conferences', limit = 1):
        text = event.title + " "+str(event.start) + reverseGeocode(event.location) + "Category: " + event.category
        conference += text
    for event in phq.events.search( start_around={'origin': '2021-12-18'},end_around={'origin':'2021-12-25'}, within='10km@'+location, category='expos', limit = 1):
        text = event.title + " "+str(event.start) + reverseGeocode(event.location) + "Category: " + event.category
        expos += text
    for event in phq.events.search( start_around={'origin': '2021-12-04'},end_around={'origin':'2021-11-11'}, within='10km@'+location, category='festivals', limit = 1):
        text = event.title + " "+ str(event.start) + reverseGeocode(event.location) + "Category: " + event.category
        festivals += text
    events = [sport,concert,arts,festivals,expos,conference]
    return events

def add_info(Address):
    event = Event(Address)
    x = get_info(Address, 15, "restaurants")
    x = top_ten(x,200)
    food_names = x['name']
    data= {"10 events":food_names, "5 Events":pd.Series(event[:-1]), "Conference":pd.Series([event[-1]])}
    df = pd.DataFrame(data)
    df.to_excel("Schedule.xlsx")
    return df

def main():
    df = pd.DataFrame(pd.read_excel("Data.xlsx"))
    analyze(df)
    new_df = pd.DataFrame(pd.read_excel("Output.xlsx"))
    chosen_location = interactive_visualizations(new_df)
    add_info(chosen_location)

if __name__ == '__main__':
    main()

