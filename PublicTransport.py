"""
FBLA Data Analysis SLC
Moksh S, Hasan R, Ethan K

This program compares PM2.5 air pollution levels with public transit usage
for different neighborhoods.
"""

#Import libraires
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load and process data
def load_data(file_path):

    return pd.read_csv(file_path)

# Filter and process PM2.5 data
def filter_pm25_data(df):

    pm25_df = df[df["Name"] == "Fine particles (PM 2.5)"]
    return pm25_df.groupby("Geo Place Name")["Data Value"].mean()

# Visualization function
def plot_comparison(pm25_data, transit_usage):

    # Filter only neighborhoods with both PM2.5 and transit data
    locations = [loc for loc in transit_usage.keys() if loc in pm25_data.index]
    pm25_values = [pm25_data[loc] for loc in locations]
    transit_values = [transit_usage[loc] for loc in locations]

    # Define bar positions
    x = np.arange(len(locations))
    bar_width = 0.4

    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - bar_width/2, pm25_values, bar_width, label="PM2.5 Levels (µg/m³)", color="salmon")
    ax.bar(x + bar_width/2, transit_values, bar_width, label="Public Transit Usage (%)", color="skyblue")

    # Labels and formatting
    ax.set_xticks(x)
    ax.set_xticklabels(locations, rotation=45, ha="right")
    ax.set_ylabel("Values")
    ax.set_title("Comparison of Public Transit Usage and PM2.5 Levels")
    ax.legend()

    # Display the plot
    plt.show()

# Main function to execute the analysis
def main():

    # Define file path
    file_path = "Air_Quality.csv"

    # Define manually provided public transit usage data
    public_transit_usage = {
        "Manhattan": 78,
        "Brooklyn": 70,
        "Queens": 60,
        "Bronx": 50,
        "Staten Island": 30
    }

    # Load and process data
    df = load_data(file_path)
    pm25_data = filter_pm25_data(df)

    # Generate visualization
    plot_comparison(pm25_data, public_transit_usage)

    # Return the processed PM2.5 data
    return pm25_data

# Run the main function and store the result
if (__name__ == "__main__"):
    pm25_results = main()
