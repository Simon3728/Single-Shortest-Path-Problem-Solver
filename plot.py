"""
This module contains a function to plot cities and their connections on a map, highlighting the shortest path and checked nodes.
"""

import matplotlib.pyplot as plt
import geopandas as gpd

def plot_cities_with_connections(city_data_df, adj_list, shapefile_path, path, checked_nodes, min_population):
    """Plots the cities with connections, highlighting the shortest path and checked nodes if provided."""
    # Load the shapefile
    gdf = gpd.read_file(shapefile_path)

    # Plotting the country and state borders
    _, ax = plt.subplots(figsize=(10, 6))
    
    # Plot state boundaries with thin lines
    gdf.boundary.plot(ax=ax, linewidth=0.5, edgecolor='black')
    
    # Plotting the cities on a map
    ax.scatter(city_data_df['lng'], city_data_df['lat'], s=10, alpha=0.5, c='blue', edgecolors='k', linewidth=1, label='Cities')
    
    # Plot lines based on the adjacency list
    for i, (city, neighbors) in enumerate(adj_list.items()):
        city_row = city_data_df[city_data_df['city'] == city].iloc[0]
        city_lat, city_lng = city_row['lat'], city_row['lng']
        for neighbor, _ in neighbors.items():
            neighbor_row = city_data_df[city_data_df['city'] == neighbor].iloc[0]
            neighbor_lat, neighbor_lng = neighbor_row['lat'], neighbor_row['lng']
            ax.plot([city_lng, neighbor_lng], [city_lat, neighbor_lat], 'grey', alpha=0.3, linewidth=0.7)

    
    # Highlight the shortest path if provided
    if path:
        for i in range(len(path) - 1):
            start_city = path[i]
            end_city = path[i+1]
            start_row = city_data_df[city_data_df['city'] == start_city].iloc[0]
            end_row = city_data_df[city_data_df['city'] == end_city].iloc[0]
            ax.plot([start_row['lng'], end_row['lng']], [start_row['lat'], end_row['lat']], 'r-', linewidth=2, label=f'Shortest Path ({len(path)})' if i == 0 else "")
        
        # Annotate the first and last city in the path
        start_city = path[0]
        end_city = path[-1]
        start_row = city_data_df[city_data_df['city'] == start_city].iloc[0]
        end_row = city_data_df[city_data_df['city'] == end_city].iloc[0]
        ax.annotate(start_city, (start_row['lng'], start_row['lat']), textcoords="offset points", xytext=(0,10), ha='center', fontsize='medium', weight='bold', color='black')
        ax.annotate(end_city, (end_row['lng'], end_row['lat']), textcoords="offset points", xytext=(0,10), ha='center', fontsize='medium', weight='bold', color='black')
    
    # Highlight checked nodes if provided
    if checked_nodes:
        checked_lats = city_data_df[city_data_df['city'].isin(checked_nodes)]['lat']
        checked_lngs = city_data_df[city_data_df['city'].isin(checked_nodes)]['lng']
        ax.scatter(checked_lngs, checked_lats, s=30, alpha=0.7, c='yellow', edgecolors='k', linewidth=1, label=f'Checked Nodes ({len(checked_nodes)})')
    
    # Adding labels and title
    plt.title(f'Cities in the US with more than {min_population} people')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    
    # Add legend
    plt.legend()
    
    plt.show()