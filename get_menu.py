from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import os
import warnings
from twilio.rest import Client

# This is not written with good programming practice. This is just written for me to get texts about what items they are pretending to have today.

warnings.filterwarnings("ignore", category=DeprecationWarning)
ffo = webdriver.FirefoxOptions()
ffo.headless = True
#todo: make directory load with $HOME
ff = webdriver.Firefox(options=ffo, executable_path=r'/home/ubuntu/dineoncampus-faster/geckodriver')
ff.get("https://dineoncampus.com/northwestern")
time.sleep(5)
location_dropdown = ff.find_element_by_id("locations__BV_toggle_")
time_dropdown = ff.find_element_by_id("periods__BV_toggle_")
station_dropdown = ff.find_element_by_id("categories__BV_toggle_")

allison_breakfast = ["Comfort 1", "Comfort 2", "Rooted 1", "Flame 3", "Bakery-Dessert"]
allison_lunch = ["Comfort 1", "Comfort 2", "Rooted 1", "Rooted 2", "Pure Eats 1", "Pure Eats 2", "Kosher", "Flame 3", "500 Degrees 1", "Bakery-Dessert"]
allison_dinner = ["Comfort 1", "Comfort 2", "Rooted 1", "Rooted 2", "Pure Eats 1", "Pure Eats 2", "Flame 3", "500 Degrees 1", "Bakery-Dessert"]

sargent_breakfast = ["Kitchen", "Rooted", "Desserts"]
sargent_lunch = ["Kitchen", "Pure Eats", "Pure Eats Fruit", "Rooted", "Flame", "500 Degrees", "Desserts"]
sargent_dinner = ["Kitchen", "Pure Eats", "Pure Eats Fruit", "Rooted", "Flame", "500 Degrees", "Desserts"]

elder_breakfast = ["Kitchen Entree", "Kitchen Sides", "Rooted", "Bakery & Dessert"]
elder_lunch = ["500 Degrees", "Flame", "Kitchen Entree", "Kitchen Sides", "Rooted", "Pure Eats", "Kosher", "Bakery & Dessert"]
elder_dinner = ["Flame", "Bakery & Dessert"]

plex_breakfast = ["Breakfast", "Bakery/Dessert"]
plex_lunch = ["Comfort", "Flame", "Pizza/Flatbread", "Bakery/Dessert"]
plex_dinner = ["Comfort", "Flame", "Pizza/Flatbread", "Bakery/Dessert"]

# Yes, using time.sleep is a bad way of waiting until items are loaded. But dineoncampus provides 0(0) way of knowing whether it's loading or loaded. I'm sure there's some way to
# Check whether it's done loading, but unfortunately this is run on a $.002/hr aws ec2 instance and I simply do not care enough.

locations = [["Allison", [allison_breakfast, allison_lunch, allison_dinner]], ["Sargent", [sargent_breakfast, sargent_lunch, sargent_dinner]], ["Elder", [elder_breakfast, elder_lunch, elder_dinner]], ["Plex West", [plex_breakfast, plex_lunch, plex_dinner]]]
meals = ["Breakfast", "Lunch", "Dinner"]
meal = meals[int(sys.argv[1])]
final_text = "Meal options for " + meal + ":\n"
for location in locations:
    location_dropdown.click()
    location_item = ff.find_elements_by_xpath("//a[contains(text(),'" + location[0] + "')]")[0]
    location_item.click()
    final_text+="Location begin\n"
    final_text+=location[0]+":\n"
    time.sleep(3)
    time_dropdown.click()
    time.sleep(.5)
    meal_item = ff.find_elements_by_xpath("//a[contains(text(),'" + meal + "')]")[0]
    meal_item.click()
    time.sleep(5)
    stations = location[1]
    if(meal=="Breakfast"):
        stations = stations[0]
    elif(meal=="Lunch"):
        stations = stations[1]
    elif(meal=="Dinner"):
        stations = stations[2]
    else:
        raise ValueError("Incorrect meal") #shouldn't trigger
    for station in stations:
        print(station)
        print("\n")
        final_text = final_text + "Station Begin\n"
        final_text = final_text + station + ":\n"
        station_dropdown.click()
        station_objs = ff.find_elements_by_xpath("//a[contains(text(),'" + station + "')]")
        if(station=="Breakfast" and location=="Plex West"):
            station_objs = [station_objs[1]]
        clicked = False
        try:
            station_objs[0].click()
            clicked = True
            all_items = ff.find_elements_by_class_name("menu-tile-item")
            for item in all_items:
                food = item.text
                food = food[0:food.index("\n")]
                if(meal=="Breakfast" and (food.find("Pancakes")==-1 and food.find("Bacon")==-1)):
                    continue
                final_text+=food+"\n"
        except:
            print("error")
        if(not clicked):
            station_dropdown.click()
        final_text+="Station End\n"
    final_text+="Location End\n"
    time.sleep(1)
path = ""
if(meal=="Breakfast"):
    path = "/home/ubuntu/menus/breakfast"
elif(meal=="Lunch"):
    path = "/home/ubuntu/menus/lunch"
elif(meal=="Dinner"):
    path = "/home/ubuntu/menus/lunch"
f = open(path, 'w')
f.write(final_text)
f.close()
#ff.save_screenshot(r'C:/Users/steve/Desktop/menu/1.png')
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
#print(pytesseract.image_to_string(r'C:\Users\steve\Desktop\menu\1.png'))
ff.close()
