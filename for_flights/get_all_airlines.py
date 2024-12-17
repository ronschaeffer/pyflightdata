import json
import os
from pyflightdata import FlightData

def save_json(data, filepath):
    """Save data to JSON file with proper formatting."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def main():
    # Initialize FlightData
    flight_data = FlightData()
    
    # Get all airlines
    print("Fetching airlines data...")
    airlines = flight_data.get_airlines()
    
    # Use the existing output directory in ~/projects/flights/output
    output_dir = '/home/ron/projects/flights/output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to file
    output_file = os.path.join(output_dir, 'airlines.json')
    print(f"Saving {len(airlines)} airlines to {output_file}")
    save_json(airlines, output_file)
    print("Done!")

if __name__ == "__main__":
    main()
