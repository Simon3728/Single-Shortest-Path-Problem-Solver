"""
This is the main entry point for the program. Main function to test and plot the Dijkstra and A* algorithms on a graph generated from city data.
"""

from get_data import extract_city_data
from make_graph import generate_random_graph
from plot import plot_cities_with_connections
from sspp_solvers import astar, dijkstra

def main():
    # File path for neccesary files
    csv_file = 'Data/uscities.csv'
    shapefile_path = 'SHP/States_shapefile.shp'

    # The minimum population, a city can have to get a node in the Graph
    min_population = 500000

    # How many degrees are desired for every node
    desired_degree = 7

    # Get City Name, Population and Location from csv File
    city_data_df = extract_city_data(csv_file, min_population)
    print(city_data_df.head())

    print(f"Total cities with a population above {min_population} in the metro area: {len(city_data_df)}")

    # Generate the Graph with all connections
    adj_list = generate_random_graph(city_data_df, desired_degree)

    # Start- and Endpoint of the Single Shortest Path problem
    start = 'Miami'
    end = 'Seattle'
    #########################################################################
    # Calculate the shortest path with the Dijkstra Algorithm
    path, total_weight, checked_nodes = dijkstra(adj_list, start, end)

    print("Shortest path:", path)
    print("Total weight:", total_weight)
    print("Checked nodes:", checked_nodes)

    # Plot the result of the Dijkstra Algorithm
    plot_cities_with_connections(city_data_df, adj_list, shapefile_path, path, checked_nodes, min_population)

    ######################################################################
    # Calculate the shortest path with the Astar Algorithm
    path, total_weight, checked_nodes = astar(adj_list, start, end, city_data_df, epsilon=2)

    print("Shortest path:", path)
    print("Total weight:", total_weight)
    print("Checked nodes:", checked_nodes)

    # Plot the result of the A* Algorithm
    plot_cities_with_connections(city_data_df, adj_list, shapefile_path, path, checked_nodes, min_population)

if __name__ == "__main__":
    main()