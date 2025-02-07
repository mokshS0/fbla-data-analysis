"""
FBLA Data Analysis SLC
Moksh S, Hasan R, Ethan K

This program shows the correlation between green spaces and pollution levels in Canada.
"""

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

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
    pollution_data = pollution_data.sort_values(by='Pollution Level', ascending=True)

    # Select a specific range of 10 cities (e.g., middle-range pollution levels)
    pollution_data = pollution_data.iloc[10:20]  # Adjust the range to select specific rows

    # Add a manual column for Green Space (%)
    manual_greenery = [80, 75, 70, 70, 50, 45, 55, 50, 55, 45]  # Replace with your own values
    pollution_data['Green Space (%)'] = manual_greenery

    return pollution_data

# Function to plot the data
def plot_data(pollution_data):

    # Create a bar plot for Green Space and a line plot for Pollution Level
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Bar plot for Green Space
    color = 'tab:green'
    ax1.set_xlabel('Area')
    ax1.set_ylabel('Green Space (%)', color=color)
    ax1.bar(pollution_data['Area'], pollution_data['Green Space (%)'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticklabels(pollution_data['Area'], rotation=45, ha='right')

    # Line plot for Pollution Level
    color = 'tab:red'
    ax2 = ax1.twinx()
    ax2.set_ylabel('Pollution Level', color=color)
    ax2.plot(pollution_data['Area'], pollution_data['Pollution Level'], color=color, marker='o')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Green Spaces and Pollution Levels in Selected Areas')
    plt.tight_layout()
    plt.show()

# Main function to execute the analysis
def main():

    file_path = 'Air_Quality.csv'
    pollution_data = load_and_process_data(file_path)
    plot_data(pollution_data)

# Run the main function
if (__name__ == '__main__'):
    main()
