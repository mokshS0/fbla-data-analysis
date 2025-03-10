"""
FBLA Data Analysis SLC
Moksh S, Hasan R, Ethan K

This program maps the pollution levels in NYC
"""

# Import libraries
import pandas as pd
import folium
from geopy.geocoders import Nominatim
import matplotlib.colors as mcolors

# Function to load and process the data
def load_and_process_data(file_path):

    # Load the CSV file
    data = pd.read_csv(file_path)

    # Filter for "Fine particles (PM 2.5)" to represent pollution levels
    pollution_data = data[data['Name'] == 'Fine particles (PM 2.5)'][['Geo Place Name', 'Data Value']]
    pollution_data = pollution_data.rename(columns={'Geo Place Name': 'Area', 'Data Value': 'Pollution Level'})

    # Aggregate pollution data by averaging for cities with multiple records
    pollution_data = pollution_data.groupby('Area', as_index=False).agg({'Pollution Level': 'mean'})

    # Sort the data by Pollution Level
    pollution_data = pollution_data.sort_values(by='Pollution Level')

    # Stratified sampling to select 50 cities
    total_cities = 50
    bins = pd.qcut(pollution_data['Pollution Level'], q=5, duplicates='drop')
    pollution_data['Category'] = bins
    sampled_data = pollution_data.groupby('Category').apply(
        lambda x: x.sample(n=min(total_cities // 5, len(x)), random_state=42)
    ).reset_index(drop=True)

    return sampled_data.drop(columns='Category')

# Function to geocode areas
def geocode_areas(pollution_data):
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
    import time

    geolocator = Nominatim(user_agent="pollution_map")

    def geocode_with_retry(area, retries=3):
        for i in range(retries):
            try:
                return geolocator.geocode(area, timeout=10)
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                print(f"Geocoding error for {area}: {e}. Retrying ({i+1}/{retries})...")
                time.sleep(2)  # Wait for 2 seconds before retrying
        return None

    pollution_data['Coordinates'] = pollution_data['Area'].apply(lambda x: geocode_with_retry(x))
    pollution_data['Latitude'] = pollution_data['Coordinates'].apply(lambda loc: loc.latitude if loc else None)
    pollution_data['Longitude'] = pollution_data['Coordinates'].apply(lambda loc: loc.longitude if loc else None)
    return pollution_data.drop(columns=['Coordinates'])

# Function to plot the map
def plot_map(pollution_data):

    # Create a base map centered around New York City
    nyc_coordinates = [40.7128, -74.0060]
    canada_map = folium.Map(location=nyc_coordinates, zoom_start=7)

    # Normalize pollution levels for color scale
    norm = mcolors.Normalize(vmin=pollution_data['Pollution Level'].min(), vmax=pollution_data['Pollution Level'].max())
    colormap = mcolors.LinearSegmentedColormap.from_list("pollution_scale", ["#ffcccc", "#990000"])  # Light to dark red

    # Add markers for each city
    for _, row in pollution_data.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            popup_text = f"{row['Area']}<br>Pollution Level: {row['Pollution Level']:.2f}"
            color = mcolors.to_hex(colormap(norm(row['Pollution Level'])))
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=15,  
                color=color,
                fill=True,
                fill_opacity=0.8,
                popup=folium.Popup(popup_text, max_width=300),
            ).add_to(canada_map)

    return canada_map

# Main function to execute the analysis
def main():

    # Define file path
    file_path = 'Air_Quality.csv'  # Replace with your actual CSV path
    pollution_data = load_and_process_data(file_path)
    pollution_data = geocode_areas(pollution_data)
    pollution_map = plot_map(pollution_data)

    # Save map to an HTML file
    pollution_map.save("pollution_map.html")
    print("Pollution map has been saved")

# Run the main function
if (__name__ == '__main__'):
    main()
