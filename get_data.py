"""
This module is responsible for extracting city data from various sources and preparing it for analysis.
"""

import pandas as pd

def extract_city_data(csv_file, min_population):
    """Extracts city data from a predefined source and returns it as a DataFrame."""
    # Read CSV File
    df = pd.read_csv(csv_file)

    # Extract important Columns 
    columns_of_interest = ['city', 'state_name', 'lat', 'lng', 'population']
    df = df[columns_of_interest]

    # Drop dublicate Cities
    df = df.drop_duplicates(subset=['city'])

    # Filter all Cities that have a population more than min_population
    df = df[df['population'] >= min_population]

    # Exclude Cities from these states since they dont fit on the shp map 
    excluded_states = ['Alaska', 'Hawaii', 'Puerto Rico', 'Guam', 'American Samoa', 'U.S. Virgin Islands', 'Northern Mariana Islands']
    df = df[~df['state_name'].isin(excluded_states)]

    return df