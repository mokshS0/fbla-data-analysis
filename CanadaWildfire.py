"""
FBLA Data Analysis SLC
Moksh S, Hasan R, Ethan K

This program shows the correlation between Canadian wildfires and NYC air pollution.
"""

# Import libraries
import matplotlib.pyplot as plt

# Function to plot the correlation between wildfires and air pollution
def plot_wildfire_air_pollution(dates, pm25_levels, wildfires):

    # Create a figure and axis
    fig, ax1 = plt.subplots()

    # Plot PM2.5 levels
    ax1.set_xlabel("Date (June 2023)")
    ax1.set_ylabel("PM2.5 Levels in NYC (µg/m³)", color="tab:red")
    ax1.plot(dates, pm25_levels, color="tab:red", marker="o", linestyle="-", label="NYC PM2.5 Levels")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    # Create a second y-axis for wildfire count
    ax2 = ax1.twinx()
    ax2.set_ylabel("Active Wildfires in Canada", color="tab:blue")
    ax2.plot(dates, wildfires, color="tab:blue", marker="s", linestyle="--", label="Canadian Wildfires")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    # Title and legend
    plt.title("Correlation Between Canadian Wildfires and NYC Air Pollution (June 2023)")
    fig.tight_layout()

    # Save the figure
    graph_path = "NYC_Wildfire_AirPollution_Graph.png"
    plt.savefig(graph_path)
    plt.show()

    return graph_path

# Main function to execute the analysis
def main():

    # Data: PM2.5 levels in NYC before, during, and after the wildfire event
    dates = ["June 1", "June 3", "June 5", "June 7", "June 9", "June 11", "June 13"]
    pm25_levels = [12, 20, 45, 117, 85, 50, 25] 

    # Data: Number of active wildfires in Canada over the same period
    wildfires = [70, 150, 200, 410, 380, 250, 130]

    # Call the function to generate the plot
    graph_path = plot_wildfire_air_pollution(dates, pm25_levels, wildfires)

    # Print path to the saved graph
    print(f"Graph saved to: {graph_path}")

# Run the main function
if (__name__ == "__main__"): 
    main()
