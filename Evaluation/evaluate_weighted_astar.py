"""
This module is used to evaluate the performance of the weighted A* Algorithm.
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

def plot_results(epsilons, results):
    """Plots the performance results of the weighted A* algorithm compared to Dijkstra's algorithm."""
    fig, ax1 = plt.subplots()

    # Define line styles for plotting
    line_styles = ['-', '--', ':']
    color_checked_nodes = 'tab:blue'
    color_error = 'tab:red'

    # Set the label for the left y-axis
    ax1.set_xlabel('Epsilon')
    ax1.set_ylabel('Checked Nodes for weighted A* in comparison with Dijkstra (%)', color=color_checked_nodes)
    ax1.tick_params(axis='y', labelcolor=color_checked_nodes)

    # Create the right y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Error (%)', color=color_error)
    ax2.tick_params(axis='y', labelcolor=color_error)

    # Plot the data for each graph configuration
    for idx, (degree, edges, nodes, average_checked_nodes_relation, average_error) in enumerate(results):
        line_style = line_styles[idx % len(line_styles)]

        ax1.plot(epsilons, average_checked_nodes_relation, color=color_checked_nodes, linestyle=line_style, label=f'Checked Nodes for desired Degree: {degree} ({edges} Edges)')
        ax2.plot(epsilons, average_error, color=color_error, linestyle=line_style, label=f'Error for desired Degree: {degree} ({edges} Edges)')

    ax1.set_xticks(epsilons)
    ax1.set_xlim([min(epsilons) - 0.1, max(epsilons) + 0.1])

    fig.tight_layout()
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title(f'Average Error and Calculation Time weighted A* vs Dijkstra for Graph with {nodes} Nodes')
    plt.show()

def get_random_city_name(df):
    """Selects a random city name from the DataFrame."""
    random_index = random.randint(0, len(df) - 1)
    random_city_name = df.iloc[random_index]['city']
    return random_city_name

def main():
    # CSV file containing city data
    csv_file = 'Data/uscities.csv'
    min_population = [100000, 500000, 1000000]
    desired_degree = [3, 7, 20]
    epsilons = [1, 1.2, 1.5, 2, 3]
    iterations = 100

    # Loop through different minimum population thresholds
    for p in min_population:
        city_data_df = extract_city_data(csv_file, p)
        city_pairs = []

        # Generate random city pairs for the evaluation
        for _ in range(iterations):
            start = get_random_city_name(city_data_df)
            end = get_random_city_name(city_data_df)
            while end == start:
                end = get_random_city_name(city_data_df)
            city_pairs.append((start, end))

        results = []
        # Loop through different desired degrees for the graph
        for d in desired_degree:
            adj_list = generate_random_graph(city_data_df, d)
            cumulative_errors = {e: 0 for e in epsilons}
            cumulative_checked_nodes = {e: 0 for e in epsilons}

            # Evaluate the algorithms for each city pair
            for start, end in city_pairs:
                # Run Dijkstra's algorithm
                _, weight, checked_nodes = dijkstra(adj_list, start, end)
                # Run weighted A* algorithm for each epsilon
                for e in epsilons:
                    _, weight_astar, checked_nodes_astar = astar(adj_list, start, end, city_data_df, epsilon=e)
                    
                    # Calculate error and add to cumulative error
                    error = ((weight_astar / weight) * 100) - 100
                    cumulative_errors[e] += error
                    
                    # Calculate node check relation and add to cumulative value
                    checked_nodes_relation = (len(checked_nodes_astar) / len(checked_nodes)) * 100
                    cumulative_checked_nodes[e] += checked_nodes_relation

            # Calculate average errors and checked nodes relations
            average_errors = [cumulative_errors[e] / iterations for e in epsilons]
            average_checked_nodes_relations = [cumulative_checked_nodes[e] / iterations for e in epsilons]

            total_edges = sum(len(neighbors) for neighbors in adj_list.values()) // 2
            results.append((d, total_edges, len(city_data_df), average_checked_nodes_relations, average_errors))

        # Plot the results
        plot_results(epsilons, results)

if __name__ == "__main__":
    main()
