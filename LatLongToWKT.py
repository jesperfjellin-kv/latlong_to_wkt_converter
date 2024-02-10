'''Script converts lat long coordinates from either user input or from a .csv file into WKT coordinates
usable with a postgis database. .csv file must be in the same directory as the python script.'''

import math
import pandas as pd


def degrees2meters(lon, lat):
    '''Math function for conversion of latitude longitude to WKT format.'''
    x = lon * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34 / 180
    return f"POINT({x} {y})"

def process_single_coordinate():
    '''Takes user input and converts it to WKT.'''
    input_str = input("Enter latitude and longitude: ")
    lat_str, lon_str = input_str.split(', ')
    lat = float(lat_str)
    lon = float(lon_str)
    result_str = degrees2meters(lon, lat)
    print(f"Converted to WKT: {result_str}")

def process_file():
    '''Opens user file, converts latitude and longitude to WKT and retains all other columns.'''
    filename = input("Enter the name of your file: ")
    df = pd.read_csv(filename)

    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['WKT'] = df.apply(lambda row: degrees2meters(row['longitude'], row['latitude']), axis=1)
        df.drop(columns=['latitude', 'longitude'], inplace=True)
        
        # Reorganizing columns to have WKT as the first column
        cols = df.columns.tolist()
        cols.remove('WKT')
        df = df[['WKT'] + cols]
    else:
        print("Error: The file does not contain 'latitude' and 'longitude' columns.")
        return

    output_file = "converted_WKT.csv"
    df.to_csv(output_file, index=False, sep=',')
    print(f"Converted coordinates saved to {output_file}")

choice = input("Do you want to convert a single instance of latitude longitude to WKT, or a file containing multiple coordinates?\nType 'single' for single instance, or 'file' for a file containing multiple coordinates: ")

if choice.lower() == 'single':
    process_single_coordinate()
elif choice.lower() == 'file':
    process_file()
else:
    print("Invalid input. Please enter 'single' or 'file'.")
