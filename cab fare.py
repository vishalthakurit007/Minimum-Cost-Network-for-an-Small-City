import networkx as nx
import matplotlib.pyplot as plt

# Pricing Variables
BASE_FARE = 30  # Base fare in ₹
FARE_PER_KM = 12  # Cost per km in ₹
AVG_SPEED_KMH = 30  # Assumed average speed (km/h)

def create_graph():
    """Creates a graph with locations and distances."""
    G = nx.Graph()

    locations = [
        "Patna Junction", "Gandhi Maidan", "AIIMS Patna", "Patna Sahib", "Bailey Road",
        "Danapur", "Kankarbagh", "Rajendra Nagar", "Boring Road", "Dak Bungalow"
    ]

    for place in locations:
        G.add_node(place)

    distances = {
        ("Patna Junction", "Gandhi Maidan"): 2.0,
        ("Patna Junction", "Rajendra Nagar"): 3.0,
        ("Gandhi Maidan", "Boring Road"): 1.5,
        ("Boring Road", "Bailey Road"): 2.5,
        ("Bailey Road", "Danapur"): 6.0,
        ("Rajendra Nagar", "Kankarbagh"): 1.8,
        ("Rajendra Nagar", "Patna Sahib"): 5.5,
        ("Patna Sahib", "AIIMS Patna"): 12.0,
        ("Dak Bungalow", "Boring Road"): 1.0,
        ("Dak Bungalow", "Gandhi Maidan"): 1.2
    }

    for (place1, place2), dist in distances.items():
        G.add_edge(place1, place2, weight=dist)

    return G, locations, distances

def dijkstra_shortest_path(graph, source, destination):
    """Finds the shortest path using Dijkstra's algorithm."""
    try:
        path = nx.shortest_path(graph, source=source, target=destination, weight="weight")
        total_distance = sum(graph[u][v]["weight"] for u, v in zip(path[:-1], path[1:]))
        return path, total_distance
    except nx.NetworkXNoPath:
        return None, float("inf")

def visualize_path(graph, path, distances, trip_distance, estimated_time, estimated_fare):
    """Creates a visualization of the shortest route."""
    pos = nx.spring_layout(graph, seed=42)  # Auto-position nodes

    plt.figure(figsize=(10, 6))
    plt.title(" Shortest Route Visualization", fontsize=14, fontweight="bold")

    # Draw full graph
    nx.draw(graph, pos, with_labels=True, node_color="lightgray", edge_color="gray", node_size=2000, font_size=10)

    # Highlight shortest path
    path_edges = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color="red", node_size=2000)
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="blue", width=2)

    # Add distance labels
    edge_labels = {edge: f"{dist} km" for edge, dist in distances.items()}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    # Show trip details inside the visualization
    details_text = (
        f" Distance: {trip_distance:.2f} km\n"
        f" Time: {estimated_time:.2f} min\n"
        f" Fare: ₹{estimated_fare:.2f}"
    )

    plt.text(0.8, 0.1, details_text, transform=plt.gca().transAxes, fontsize=12,
             bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.5"))

    plt.show()

# Create Graph
G, location_list, distances = create_graph()

# User Input
print("\n🚖 Cab Fare Estimator with Visualization 🚖")
print("\nAvailable Locations:")
for loc in location_list:
    print(f"- {loc}")

source_location = input("\nEnter Source Location: ")
destination_location = input("Enter Destination Location: ")

if source_location not in location_list or destination_location not in location_list:
    print(" Invalid locations! Choose from the available list.")
    exit()

# Find Shortest Path using Dijkstra’s Algorithm
shortest_path, trip_distance = dijkstra_shortest_path(G, source_location, destination_location)

if not shortest_path:
    print(" No path found between the locations.")
    exit()

# Estimate Fare & Travel Time
estimated_fare = BASE_FARE + (FARE_PER_KM * trip_distance)
estimated_time = (trip_distance / AVG_SPEED_KMH) * 60  # Convert hours to minutes

# Display Fare & Route
print(f"\n Shortest Route: {' → '.join(shortest_path)}")
print(f" Distance: {trip_distance:.2f} km")
print(f" Estimated Time: {estimated_time:.2f} minutes")
print(f" Estimated Fare: ₹{estimated_fare:.2f}")

# Visualize Path
visualize_path(G, shortest_path, distances, trip_distance, estimated_time, estimated_fare)
