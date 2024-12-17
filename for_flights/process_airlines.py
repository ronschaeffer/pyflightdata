import json
import os

def parse_callsign(callsign_str):
    """Parse callsign string to extract IATA and ICAO codes"""
    if not callsign_str:
        return None, None
        
    # Handle format "2I / CSB"
    if " / " in callsign_str:
        iata, icao = callsign_str.split(" / ")
        return iata, icao
    
    # Handle format "CSB"
    return None, callsign_str

def process_airline(airline):
    """Transform airline dictionary to new format"""
    iata_code, icao_code = parse_callsign(airline.get('callsign', ''))
    
    return {
        "iata_code": iata_code or "",
        "name": airline.get('title', ''),
        "icao_code": icao_code or "",
        "airline_callsign": "",
        "country": "",
        "country_code": ""
    }

def main():
    # Input/output paths
    input_dir = '/home/ron/projects/flights/output'
    output_dir = '/home/ron/projects/flights/output/processed'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read input file
    input_file = os.path.join(input_dir, 'airlines.json')
    output_file = os.path.join(output_dir, 'airlines_processed.json')
    
    print(f"Reading airlines from {input_file}")
    with open(input_file, 'r') as f:
        airlines = json.load(f)
    
    # Process airlines
    processed_airlines = []
    for airline in airlines:
        processed_airline = process_airline(airline)
        if processed_airline:
            processed_airlines.append(processed_airline)
    
    # Save processed data
    print(f"Saving {len(processed_airlines)} processed airlines to {output_file}")
    with open(output_file, 'w') as f:
        json.dump(processed_airlines, f, indent=4)
    
    print("Done!")

if __name__ == "__main__":
    main()
