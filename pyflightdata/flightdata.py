from .common_fr24 import REG_BASE, FLT_BASE, AIRPORT_BASE, AIRLINE_BASE, AIRLINE_FLT_BASE, LOGIN_URL, ROOT, get_data, get_countries_data
from .common_fr24 import get_airports_data, get_aircraft_data, get_airlines_data, get_airline_fleet_data, get_airline_flight_data
from common import put_to_page, json_loads_byteified

#Flight related information - primarily from flightradar24
def get_history_by_flight_number(flight_number,token=''):
    url = FLT_BASE.format(flight_number,token)
    return get_data(url)

def get_history_by_tail_number(tail_number,token=''):
    url = REG_BASE.format(tail_number,token)
    return get_data(url, True)

def get_countries():
    return get_countries_data()

def get_airports(country):
    url = AIRPORT_BASE.format(country)
    return get_airports_data(url)

def get_info_by_tail_number(tail_number):
    url = AIRLINE_BASE.format(tail_number)
    return get_aircraft_data(url)

def get_airlines():
    url = AIRLINE_BASE.format('')
    return get_airlines_data(url)

def get_fleet(airline_key):
    url = AIRLINE_BASE.format(airline_key)
    return get_airline_fleet_data(url)

def get_flights(airline_key):
    url = AIRLINE_FLT_BASE.format(airline_key)
    return get_airline_flight_data(url)

#Route and range related information from gcmap
def get_range_map(airport,*range,**options):
    pass
    
def get_path_map(*pathsegment,**options):
    pass

#Pictures from jetphotos and airliners.net
def get_images_by_tail(tail_number):
    pass
    
def login(user,password):
    from requests import Session
    session=Session()
    response = session.post(
        url=LOGIN_URL,
        data={
            'email': user,
            'password': password,
            'remember': 'false',
            'type': 'web'
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'
        }
    )
    response = json_loads_byteified(response.content) if response.status_code==200 else None
    if unicode('token') in response.keys():
        return response[unicode('token')]