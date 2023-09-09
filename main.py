#Importing libraries
import requests
from tkinter import ttk
from tkinter import *
import json
from io import BytesIO
from PIL import Image , ImageTk
import ipdata
#End of importing libraries
#Finding the current location of user
ipdata.api_key ="9173133373ae11f4b6f5fb3227f180ee220fae74b897f8ab3be0f672"
data = ipdata.lookup()
longitude = data.longitude
latitude = data.latitude

#End of finding the location



#Generating the country and cities for user
country_api = "https://api.countrystatecity.in/v1/countries"

headers = {
    'X-CSCAPI-KEY': 'ZlJ2MkpINmZud0p4ajVQOFRiMnZXb2hqZWJNZUdtaWRWbzdoQkRNMA=='
}

def find_city_location():
    lat_and_lon_request = requests.get(
        'https://api.openweathermap.org/geo/1.0/direct?q={0}&limit=5&appid=9045a97df77bbf9ef63698b29544e60c'.format(
            city_combobox.get()))
    json_lat_and_lon_request = json.loads(lat_and_lon_request.text)
    lon_of_city = json_lat_and_lon_request[0]["lon"]
    lat_of_city = json_lat_and_lon_request[0]["lat"]
    new_weather_request = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=Metric&appid={2}".format(lat_of_city,
                                                                                                        lon_of_city,
                                                                                                        weather_api))
    new_weather_data = new_weather_request.text
    new_weather_json = json.loads(new_weather_data)
    #show selected location datas
    selected_location_condition.configure(text=new_weather_json["weather"][0]["main"])
    selected_location.configure(text=new_weather_json["name"])
        #generating an icon for condition of weather
    weather_icon = requests.get('https://openweathermap.org/img/wn/{0}.png'.format(new_weather_json['weather'][0]['icon']))
    image_generator = Image.open(BytesIO(weather_icon.content))
    tk_image = ImageTk.PhotoImage(image_generator)
    condition_icon.create_image(5,5 , anchor = "w" , image=tk_image)
    #End of Creating icon
    selected_location_condition_description.configure(text=new_weather_json["weather"][0]["description"])
    selected_location_tempereture.configure(text=new_weather_json["main"]["temp"])
    selected_location_humidity.configure(text=str(new_weather_json['main']["humidity"])+"%")
    selected_location_wind_speed.configure(text=new_weather_json['wind']['speed'])
    #end of showing the data and replacing with the default datas
def generating_cities(event):
    city_combobox.configure(values=())
    selected_item = country_combobox.get()
    if selected_item:
        iso2 = selected_item[-2:]
        city_api = "https://api.countrystatecity.in/v1/countries/{0}/cities".format(iso2)
        response_city = requests.request("GET", city_api, headers=headers)
        city_json = json.loads(response_city.text)
        for city in city_json:
            city_combobox['values'] = (*city_combobox['values'], city["name"])

#End of Generating the countries and cities



#Generating weather datas
weather_api = "9045a97df77bbf9ef63698b29544e60c"
weather_request = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=Metric&appid={2}".format(latitude , longitude , weather_api))
weather_data = weather_request.text
weather_data_json = json.loads(weather_data)

#End of generating weather datas




#Making a window using tkinter to show the collected data
window = Tk()
window.title("Current weather using python")
window.geometry("800x600")
window.minsize(600,350)
window.resizable(width=False,height=True)

location_label = Label(window , text="Location: ")
location_label.grid(row = 0 , column =0 , pady =2 , padx = (5,0) , sticky = "e")
selected_location = Label(window , text="")
selected_location.grid(row =0 , column = 1 , pady=2 , padx=(0,0) , sticky ="w")


current_condition_label = Label(window , text="Current condition: ")
current_condition_label.grid(row = 1 , column =0 , pady =2 , padx = (5,0) , sticky = "e")
selected_location_condition = Label(window , text="")
selected_location_condition.grid(row =1, column = 1 , pady=2 , padx=(0,0) , sticky ="w")
condition_icon = Canvas(window)
condition_icon.grid(row=1 , column=2 , pady=2 , padx=(5,0) , rowspan = 8 )


current_condition_description_label = Label(window , text="Current condition description: ")
current_condition_description_label.grid(row = 2 , column =0 , pady =2 , padx = (5,0) , sticky = "e")
selected_location_condition_description = Label(window , text="")
selected_location_condition_description.grid(row =2, column = 1 , pady=2 , padx=(0,0) , sticky ="w")


todays_tempereture_label = Label(window , text="Today's tempereture: ")
todays_tempereture_label.grid(row = 3 , column =0 , pady =2 , padx = (5,0) , sticky = "e")
selected_location_tempereture = Label(window , text="")
selected_location_tempereture.grid(row =3, column = 1 , pady=2 , padx=(0,0) , sticky ="w")


humidity_label = Label(window , text="Humidity: ")
humidity_label.grid(row = 4 , column =0 , pady =2 , padx = (5,0) , sticky = "e")
selected_location_humidity = Label(window , text="")
selected_location_humidity.grid(row =4, column = 1 , pady=2 , padx=(0,0) , sticky ="w")



wind_speed_label = Label(window , text="Wind speed: ")
wind_speed_label.grid(row = 5 , column =0 , pady =2 , padx = (5,0) , sticky = "e")
selected_location_wind_speed = Label(window , text="")
selected_location_wind_speed.grid(row =5, column = 1 , pady=2 , padx=(0,0) , sticky ="w")


country_label = Label(window, text="Country: ")
country_label.grid(row=6 , column = 0 , pady=2, padx=(5,0) , sticky ="e")

country_combobox = ttk.Combobox(window)
country_combobox.grid(row=6 ,column = 1 , pady = 2 , padx=(0,0) , sticky = "w")

response_country = requests.request("GET", country_api, headers=headers)

country_json = json.loads(response_country.text)
for country in country_json:
    country_combobox['values'] = (*country_combobox['values'] , country["name"]+" "+country["iso2"])

city_label = Label(window , text="City: ")
city_label.grid(row=7 , column = 0 , pady = 2 , padx = (5,0), sticky="e")
city_combobox = ttk.Combobox(window)
city_combobox.grid(row =7, column =1 , pady =2 , padx=(0,0) , sticky ="w")

button_to_search = Button(window , command=find_city_location , text="search")
button_to_search.grid(row=8 , column =1 , pady =2 , padx = (5,5))
country_combobox.bind("<<ComboboxSelected>>", generating_cities)



#show default location datas
selected_location_condition.configure(text=weather_data_json["weather"][0]["main"])
selected_location.configure(text=weather_data_json["name"])
    #generating an icon for condition of weather
weather_icon = requests.get('https://openweathermap.org/img/wn/{0}.png'.format(weather_data_json['weather'][0]['icon']))
image_generator = Image.open(BytesIO(weather_icon.content))
tk_image = ImageTk.PhotoImage(image_generator)
condition_icon.create_image(5,5 , anchor = "w" , image=tk_image)
    #End of Creating icon
selected_location_condition_description.configure(text=weather_data_json["weather"][0]["description"])
selected_location_tempereture.configure(text=weather_data_json["main"]["temp"])
selected_location_humidity.configure(text=str(weather_data_json['main']["humidity"])+"%")
selected_location_wind_speed.configure(text=weather_data_json['wind']['speed'])


window.mainloop()
#End of making a window
