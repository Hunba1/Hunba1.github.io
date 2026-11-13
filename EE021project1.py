import matplotlib.pyplot as plt
import openmeteo_requests
import csv
import pandas as pd

openmeteo = openmeteo_requests.Client()

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 37.3259,
	"longitude": 120.4999,
	"hourly": "temperature_2m",
	"timezone": "America/Los_Angeles",
	"past_days": 7,
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
    "past_days" : 30,
    "forecast_days" : 0,
}
responses = openmeteo.weather_api(url, params = params)
response = responses[0]

hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	).tz_convert(response.Timezone().decode())
}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_dataframe = pd.DataFrame(data=hourly_data)

with open("weather.csv", "w", newline=""):
	weather_data = hourly_dataframe.to_csv("weather.csv", index=False)

with open("weather.csv", "r") as file:
    weather_data = pd.read_csv(file)

print("You are able to choose the temperature data for the following timepoints, \n1. Past day, \n2. Past week, \n3. Past month. ")

graph_choice = input("Please choose which time stamp you would like to see displayed:")
if graph_choice == "1":
    selected_data = weather_data.tail(24)
    dates = pd.to_datetime(selected_data["date"]).dt.tz_localize(None)
    temperature = (selected_data["temperature_2m"])
    plt.plot(dates, temperature)
    plt.title("Temperature over the past 24 hours")
    plt.xlabel("Dates")
    plt.ylabel("Temperature(in farenheit)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
elif graph_choice == "2":
    selected_data = weather_data.tail(168)
    dates = pd.to_datetime(selected_data["date"]).dt.tz_localize(None)
    temperature = (selected_data["temperature_2m"])
    plt.plot(dates, temperature)
    plt.title("Temperature over the past 7 days")
    plt.xlabel("Dates")
    plt.ylabel("Temperature(in farenheit)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
elif graph_choice == "3":
    selected_data = weather_data.tail(720)
    dates = pd.to_datetime(selected_data["date"]).dt.tz_localize(None)
    temperature = (selected_data["temperature_2m"])
    plt.plot(dates, temperature)
    plt.title("Temperature over the past 30 days")
    plt.xlabel("Dates")
    plt.ylabel("Temperature(in farenheit)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("invalid graph choice, please pick an input 1-3")