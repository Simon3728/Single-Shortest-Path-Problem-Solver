"""
This module is used to evaluate the performance of the Dijkstra and A* Algorithm.
"""

import sys
import os

# Add the parent directory to the sys.path to import custom modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from get_data import extract_city_data
from make_graph import generate_random_graph
from sspp_solvers import astar, dijkstra
import random
import matplotlib.pyplot as plt
import numpy as np

def get_random_city_name(df):
    """Selects a random city name from the DataFrame."""
    random_index = random.randint(0, len(df) - 1)
    random_city_name = df.iloc[random_index]['city']
    return random_city_name

def plot_result(total_edges, avg_checked_nodes_dijkstra, avg_checked_nodes_astar, nodes):
    """Plots the average number of checked nodes for different path lengths for Dijkstra and A* algorithms."""
    
    # Sort path lengths
    path_lengths = sorted(avg_checked_nodes_dijkstra.keys())
    avg_nodes_dijkstra = [avg_checked_nodes_dijkstra[length] for length in path_lengths]
    avg_nodes_astar = [avg_checked_nodes_astar[length] for length in path_lengths]
    
    # Define bar width for plotting
    bar_width = 0.35
    
    # Set the positions of the bars
    r1 = np.arange(len(path_lengths))
    r2 = [x + bar_width for x in r1]
    
    # Plot the bars for Dijkstra and A* algorithms
    plt.figure(figsize=(10, 6))
    plt.bar(r1, avg_nodes_dijkstra, color='b', width=bar_width, edgecolor='grey', label='Dijkstra')
    plt.bar(r2, avg_nodes_astar, color='r', width=bar_width, edgecolor='grey', label='A*')

    # Add labels and title
    plt.xlabel('Path Length', fontweight='bold')
    plt.ylabel('Average Number of Checked Nodes', fontweight='bold')
    plt.title(f'Efficiency Dijkstra vs A* in a Graph with {nodes} Nodes, {total_edges} Edges', fontweight='bold')

    # Add a legend
    plt.legend()

    # Add grid
    plt.grid(True)

    # Show the plot
    plt.show()

def main():
    # CSV file containing city data
    csv_file = 'Data/uscities.csv'
    min_population = 100000
    desired_degree = [3, 7, 20]
    iterations = 200
    city_pairs = []

    # Extract city data from the CSV file
    city_data_df = extract_city_data(csv_file, min_population)

    # Generate random city pairs for the evaluation
    for _ in range(iterations):
        start = get_random_city_name(city_data_df)
        end = get_random_city_name(city_data_df)
        while end == start:
            end = get_random_city_name(city_data_df)
        city_pairs.append((start, end))

    # Evaluate the algorithms for each desired degree
    for d in desired_degree:
        # Generate a random graph with the given degree
        adj_list = generate_random_graph(city_data_df, d)
        total_edges = sum(len(neighbors) for neighbors in adj_list.values()) // 2

        # Dictionaries to store path lengths and checked nodes
        path_data_dijkstra = {}
        path_data_astar = {}

        # Run the algorithms for each city pair
        for start, end in city_pairs:
            # Run Dijkstra's algorithm
            path_dijkstra, _, checked_nodes_dijkstra = dijkstra(adj_list, start, end)
            length_dijkstra = len(path_dijkstra)
            checked_dijkstra = len(checked_nodes_dijkstra)

            # Run A* algorithm
            path_astar, _, checked_nodes_astar = astar(adj_list, start, end, city_data_df)
            length_astar = len(path_astar)
            checked_astar = len(checked_nodes_astar)

            # Store results for Dijkstra
            if length_dijkstra not in path_data_dijkstra:
                path_data_dijkstra[length_dijkstra] = []
            path_data_dijkstra[length_dijkstra].append(checked_dijkstra)

            # Store results for A*
            if length_astar not in path_data_astar:
                path_data_astar[length_astar] = []
            path_data_astar[length_astar].append(checked_astar)

        # Calculate average number of checked nodes for each path length
        avg_checked_nodes_dijkstra = {length: sum(nodes) / len(nodes) for length, nodes in path_data_dijkstra.items()}
        avg_checked_nodes_astar = {length: sum(nodes) / len(nodes) for length, nodes in path_data_astar.items()}

        # Plot the results
        plot_result(total_edges, avg_checked_nodes_dijkstra, avg_checked_nodes_astar, len(city_data_df))

if __name__ == "__main__":
    main()
