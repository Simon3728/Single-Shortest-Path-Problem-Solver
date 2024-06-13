"""
This module contains functions for generating and manipulating graphs based on city data.
"""

import heapq
from math import radians, sin, cos, sqrt, atan2
import pandas as pd

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two points on the Earth's surface."""
    R = 6371.0  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)  # Difference in latitude in radians
    dlon = radians(lon2 - lon1)  # Difference in longitude in radians
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2  # Haversine formula
    c = 2 * atan2(sqrt(a), sqrt(1 - a))  # Angular distance in radians
    return R * c  # Distance in kilometers

# Generate Minimum Spanning Tree (MST) using Prim's Algorithm
def generate_mst(cities):
    """Generate a Minimum Spanning Tree (MST) using Prim's algorithm."""
    num_cities = len(cities)  # Number of cities
    edges = []  # List to store the edges of the MST
    in_mst = [False] * num_cities  # Boolean array to track if a city is included in the MST
    min_edge = []  # Min-heap to get the edge with the smallest weight

    # Start from the first city
    in_mst[0] = True
    for i in range(1, num_cities):
        dist = haversine(cities[0][1], cities[0][2], cities[i][1], cities[i][2])
        heapq.heappush(min_edge, (dist, i, 0))

    # While the MST does not include all cities
    while len(edges) < num_cities - 1:
        weight, to, frm = heapq.heappop(min_edge)  # Get the edge with the smallest weight
        if not in_mst[to]:  # If the target city is not in the MST
            in_mst[to] = True  # Include the target city in the MST
            edges.append((frm, to, weight))  # Add the edge to the MST
            for next_to in range(num_cities):
                if not in_mst[next_to]:  # If the next city is not in the MST
                    dist = haversine(cities[to][1], cities[to][2], cities[next_to][1], cities[next_to][2])
                    heapq.heappush(min_edge, (dist, next_to, to))  # Add the edge to the min-heap
    return edges

# Create adjacency list using city names from the edges of the MST
def create_adjacency_list(edges, cities):
    """Create an adjacency list from the edges of the MST."""
    adj_list = {}
    for frm, to, weight in edges:
        frm_city = cities[frm][0]
        to_city = cities[to][0]
        if frm_city not in adj_list:
            adj_list[frm_city] = {}
        if to_city not in adj_list:
            adj_list[to_city] = {}
        adj_list[frm_city][to_city] = weight  # Add the edge to the adjacency list
        adj_list[to_city][frm_city] = weight  # Since the graph is undirected, add the reverse edge as well
    return adj_list

def add_edges_to_degree(adj_list, cities, desired_degree):
    """Add edges to the adjacency list to achieve the desired degree for each node."""
    
    for city in cities:
        city_name = city[0]
        current_degree = len(adj_list[city_name])
        if current_degree >= desired_degree:
            continue
        
        # Calculate the distance from the city to all other cities
        nearest_cities = []
        for other_city in cities:
            if city_name != other_city[0] and other_city[0] not in adj_list[city_name]:
                dist = haversine(city[1], city[2], other_city[1], other_city[2])
                nearest_cities.append((dist, other_city[0]))
        
        # Sort cities by distance
        nearest_cities.sort()  
        
        # Add edges to the nearest cities until the desired degree is achieved
        for dist, nearest_city in nearest_cities:
            if len(adj_list[city_name]) < desired_degree:
                adj_list[city_name][nearest_city] = dist
                adj_list[nearest_city][city_name] = dist
    
    return adj_list

def generate_random_graph(city_data_df, desired_degree):
    """Generate a random graph with a given degree for each node."""
    # Extract city data from DataFrame
    cities = city_data_df[['city', 'lat', 'lng']].values.tolist()  

    # Generate Minimal Spanning Tree
    mst_edges = generate_mst(cities) 

    # Create adjacency list from MST edges
    adj_list = create_adjacency_list(mst_edges, cities) 

    # Add edges to achieve the desired degree
    adj_list = add_edges_to_degree(adj_list, cities, desired_degree)  

    return adj_list
