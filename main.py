
import requests
from datetime import datetime
import os

#API_KEY = os.environ['TELEAPI_KEY']
#COWIN_API_ENDPOINT = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
COWIN_API_ENDPOINT = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"

TELEGRAM_END_POINT= "https://api.telegram.org/bot5093725802:AAGdG9fDKcGQ2x8FH2W9qkYL-95vHawre_U/sendMessage?chat_id=-666655655&text="
today_date = datetime.now().strftime("%d/%m/%Y")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def session_data (center,session):
    return {
        "name" : center["name"],

        "date": session["date"],
        "available_capacity": session["available_capacity"],
        "min_age_limit": session["min_age_limit"],
        "vaccine" : session["vaccine"]

    }

def get_session(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield session_data(center,session)

def is_available(session):
    return session["available_capacity"] 
    #> 900

def is_eighteen_plus(session):
    return session["min_age_limit"] == 15


def fetch_data(today_date):



      appointment_params = {
          #"district_id": 684,
          "pincode":247001,
          "date": today_date,
      }
      response = requests.get(COWIN_API_ENDPOINT, params = appointment_params,headers = headers)
      data = response.json()
      #print(response.status_code)
      #return (data)
      return[session for session in get_session(data) if is_eighteen_plus(session) and is_available(session)]


def create_output(availability_status):
    return f"{availability_status['date']} - {availability_status['name']} ({availability_status['available_capacity']})-{availability_status['vaccine']}"


#print(fetch_data(datetime.now().strftime("%d/%m/%Y")))

content = "\n".join([create_output(availability_status) for availability_status in fetch_data(today_date)])
#print(content)


def send_message_tele(content):
    final_url = TELEGRAM_END_POINT + content
    resp = requests.get(final_url)
    print(resp)


if not content:
    print("No availability")
else:
    send_message_tele(content)
