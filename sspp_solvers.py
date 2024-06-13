"""
This module contains implementations of shortest path algorithms such as Dijkstra's and A*.
"""

from heapq import heappop, heappush
from make_graph import haversine

def dijkstra(adj_list, start, end):
    """Implements Dijkstra's algorithm to find the shortest path between start and end nodes."""
    
    # Initialize the distance to all nodes as infinity and previous nodes as None
    distances = {node: float('inf') for node in adj_list}
    previous_nodes = {node: None for node in adj_list}
    distances[start] = 0  # The distance to the start node is 0
    
    # Priority queue to hold the nodes to explore, initialized with the start node
    priority_queue = [(0, start)]
    
    # List to keep track of the nodes that have been checked
    checked_nodes = []
    
    while priority_queue:
        # Pop the node with the smallest distance from the queue
        current_distance, current_node = heappop(priority_queue)
        checked_nodes.append(current_node)

        # If the end node is reached, reconstruct the path
        if current_node == end:
            path = []
            while previous_nodes[current_node] is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]
            path.insert(0, start)
            return path, distances[end], checked_nodes
        
        # If the current node's distance is greater than the stored distance, skip this node
        if current_distance > distances[current_node]:
            continue
        
        # Explore the neighbors of the current node
        for neighbor, weight in adj_list[current_node].items():
            distance = current_distance + weight
            
            # If a shorter path to the neighbor is found, update the distance and queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heappush(priority_queue, (distance, neighbor))
    
    # If the end node is not reachable, return empty path and infinite distance
    return [], float('inf'), checked_nodes

def heuristic(node1, node2, cities_df):
    """Implements the heuristic for the A* algorithm, which is the estimated distance from the current node to the end node."""
    
    city1 = cities_df[cities_df['city'] == node1].iloc[0]
    city2 = cities_df[cities_df['city'] == node2].iloc[0]
    return haversine(city1['lat'], city1['lng'], city2['lat'], city2['lng'])

def astar(graph, start, end, cities_df, epsilon=1.0):
    """Implements the A* algorithm to find the shortest path between start and end nodes with a given epsilon."""
    
    # Priority queue to hold nodes to explore, initialized with the start node and its heuristic cost
    open_list = []
    heappush(open_list, (0, start))
    
    # Dictionary to reconstruct the path
    came_from = {}
    
    # Initialize g_score (cost from start to each node) and f_score (g_score + heuristic)
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, end, cities_df) * epsilon
    
    # List to keep track of the nodes that have been checked
    checked_nodes = []

    while open_list:
        # Pop the node with the smallest f_score from the queue
        _, current = heappop(open_list)
        checked_nodes.append(current)

        # If the end node is reached, reconstruct the path
        if current == end:
            path = []
            total_weight = g_score[current]
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, total_weight, checked_nodes

        # Explore the neighbors of the current node
        for neighbor, weight in graph[current].items():
            tentative_g_score = g_score[current] + weight
            
            # If a shorter path to the neighbor is found, update g_score, f_score, and queue
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end, cities_df) * epsilon
                heappush(open_list, (f_score[neighbor], neighbor))

    # If the end node is not reachable, return None and infinite weight
    return None, float('inf'), checked_nodes
