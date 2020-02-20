#weather_email_v1.0

#importing modules
import smtplib
import datetime
import requests
import json
from email.message import EmailMessage

#USER MUST CHANGE THESE VARIABLES
MY_ADDRESS = "********"         #sender's gmail address
PASSWORD = "********"           #sender's gmail password (2fa must be off and "less secure app access" must be on)
RECIPIENT_ADDRESS = "********"  #gmail address for recipient
api_key = "********"            #API key for account at openweathermap.org

#do not change these variables
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "Boston" 
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

#connect and authenticate to SMTP server
print("Connecting to SMTP server...")
server = smtplib.SMTP(host='smtp.gmail.com', port=587)
server.starttls()
print("Connection successful.")
print("Logging in...")
server.login(MY_ADDRESS, PASSWORD)
print("Login successful.")

#get temperature via openweathermap API
response = requests.get(complete_url)           #sending url request to openweathermap
weather_api_response = response.json()          #convert response from javascript to python
city_response = weather_api_response["name"]    #get city name from API response
temp_k = weather_api_response["main"]["temp"]   #get temperature (in kelvin) from API response
temp_f = 9/5 *(temp_k - 273) + 32               #convert temperature from kelvin to fahrenheit

#setting email message parameters
msg = EmailMessage()                                            #delare msg variable
msg['Subject'] = city_response + " temperature update"
msg['From'] = MY_ADDRESS
msg['To'] = RECIPIENT_ADDRESS
msg.set_content("The current date and time is: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n" +
                "The current temperature in " + city_response + " is: " + str(int(round(temp_f, 0))) + " F")

#sending email message
print("Sending email...")
server.send_message(msg)
print("Email sent.")

server.quit() #end of program