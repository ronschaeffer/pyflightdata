import json
from pyflightdata import FlightData

def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_json(data, filepath):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def lookup_airlines(missing_data, flight_data):
    new_airlines = {}
    found_airlines = []
    airlines = flight_data.get_airlines()  # Get full list of airlines
    
    for icao_code in missing_data.get('airlines', {}):
        print(f"Looking up airline for ICAO code: {icao_code}")
        found = [airline for airline in airlines if airline.get('callsign', '').endswith('/' + icao_code)]
        if found:
            airline_info = found[0]
            new_airlines[icao_code] = airline_info
            found_airlines.append({"airline_icao": icao_code})
            print(f"Found airline: {airline_info}")
        else:
            print(f"No data found for airline ICAO code: {icao_code}")
    return new_airlines, found_airlines

def lookup_aircraft(missing_data, flight_data):
    new_aircraft = {}
    found_aircraft = []
    for icao_code, data in missing_data.get('aircraft', {}).items():
        # Get registration from stored data
        reg = data.get('reg', '')
        if reg:
            print(f"Looking up aircraft registration: {reg} for type: {icao_code}")
            aircraft_info = flight_data.get_info_by_tail_number(reg)
            if aircraft_info:
                new_aircraft[icao_code] = aircraft_info
                found_aircraft.append({"aircraft_icao": icao_code, "registration": reg})
                print(f"Found aircraft: {aircraft_info}")
            else:
                print(f"No data found for aircraft registration: {reg}")
        else:
            print(f"No registration found for aircraft type: {icao_code}")
    return new_aircraft, found_aircraft

def lookup_airports(missing_data, flight_data):
    new_airports = {}
    found_airports = []
    for iata_code in missing_data.get('airports', {}):
        print(f"Looking up airport for IATA code: {iata_code}")
        if iata_code not in new_airports:
            airports = flight_data.get_airports('any')  # Search all countries
            found = [airport for airport in airports if airport.get('iata') == iata_code]
            if found:
                airport_info = found[0]
                new_airports[iata_code] = {
                    "country_code": airport_info.get("country_code"),
                    "subdivision": airport_info.get("subdivision"),
                    "elevation": airport_info.get("elevation"), 
                    "latitude": airport_info.get("lat"),
                    "longitude": airport_info.get("lon"),
                    "ts": None,  # Not available in API
                    "lid": None  # Not available in API
                }
                found_airports.append({"airport_iata": iata_code})
                print(f"Found airport: {airport_info}")
            else:
                print(f"No data found for airport IATA code: {iata_code}")
    return new_airports, found_airports

def main():
    flight_data = FlightData()
    missing_data = load_json('/home/ron/projects/flights/output/missing.json')

    print(f"Total missing airlines: {len(missing_data.get('airlines', {}))}")
    print(f"Total missing aircraft: {len(missing_data.get('aircraft', {}))}")
    print(f"Total missing airports: {len(missing_data.get('airports', {}))}")

    new_airlines, found_airlines = lookup_airlines(missing_data, flight_data)
    new_aircraft, found_aircraft = lookup_aircraft(missing_data, flight_data)
    new_airports, found_airports = lookup_airports(missing_data, flight_data)

    save_json(new_airlines, '/home/ron/projects/flights/output/new_airlines.json')
    save_json(new_aircraft, '/home/ron/projects/flights/output/new_aircraft.json')
    save_json(new_airports, '/home/ron/projects/flights/output/new_airports.json')

    found_data = {
        "airlines": found_airlines,
        "aircraft": found_aircraft,
        "airports": found_airports
    }
    save_json(found_data, '/home/ron/projects/flights/output/found.json')

if __name__ == "__main__":
    main()
