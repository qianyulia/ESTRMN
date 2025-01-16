import numpy as np
import ms_entropy as me
import pandas as pd
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain  # Import Louvain community detection method

# Read parent and product spectra files
parent_df = pd.read_excel("parent.xlsx")
product_df = pd.read_excel("product.xlsx")

# Helper function to process spectra
def process_spectrum(spectrum_str):
    spectrum = [np.array(item.split(":"), dtype=float) for item in spectrum_str.split(" ")]
    return me.clean_spectrum(spectrum, min_ms2_difference_in_da=0.01)

# Build parent and product spectral libraries
parent_spectra = [{
    "id": row["ID"],
    "precursor_mz": row["mz"],
    "peaks": process_spectrum(row["MS2"]),
    "type": "parent"
} for _, row in parent_df.iterrows()]

product_spectra = [{
    "id": row["ID"],
    "precursor_mz": row["mz"],
    "peaks": process_spectrum(row["MS2"]),
    "type": "product"
} for _, row in product_df.iterrows()]

# Combine the parent and product spectra libraries
spectral_library_all = parent_spectra + product_spectra

# Calculate similarities between all pairs of parent and product spectra
similarid = set()  # Directly using set to remove duplicates
for parent in tqdm(parent_spectra):
    for product in product_spectra:
        similarity = me.calculate_entropy_similarity(parent["peaks"], product["peaks"], ms2_tolerance_in_da=0.01)
        if similarity > 0.5:
            similarid.add(parent["id"])  # Add to set
            similarid.add(product["id"])  # Add to set

# Create a mapping from ID to index in the spectral library
id_to_index = {spectrum["id"]: idx for idx, spectrum in enumerate(spectral_library_all)}

# Calculate similarities between all pairs of similar IDs
similarities = []
similarid_list = list(similarid)  # Convert the set to a list for indexing

for i in range(len(similarid_list)):
    for j in range(i + 1, len(similarid_list)):
        idx_i = id_to_index[similarid_list[i]]
        idx_j = id_to_index[similarid_list[j]]
        X = me.calculate_entropy_similarity(spectral_library_all[idx_i]["peaks"], spectral_library_all[idx_j]["peaks"], ms2_tolerance_in_da=0.01)
        source = spectral_library_all[idx_i]["id"]
        target = spectral_library_all[idx_j]["id"]
        if X > 0.5:
            similarities.append({"source": source, "target": target, "similarity": X})

# Save the similarities to a CSV file
similarities_df = pd.DataFrame(similarities)
similarities_df.to_csv("similarities.csv", index=False)

# Get all connected nodes based on similarities
connected_nodes = {sim["source"] for sim in similarities} | {sim["target"] for sim in similarities}

# Create the graph and add edges based on similarities
G = nx.Graph()
for sim in similarities:
    if sim["source"] in connected_nodes and sim["target"] in connected_nodes:
        G.add_edge(sim["source"], sim["target"], weight=sim["similarity"])

# Apply Louvain community detection algorithm
partition = community_louvain.best_partition(G)

# Create a color map for each community
community_colors = [partition[node] for node in G.nodes()]

# Define custom colors for communities
custom_colors = ['#B50A2AFF', '#0E84B4FF', '#E48C2AFF', '#574A5EFF', "#14454CFF", "#E75B64FF"]

# Map community numbers to custom colors
node_colors = [custom_colors[community_colors[i] % len(custom_colors)] for i in range(len(community_colors))]

# Get node layout with adjusted spring constant to reduce repulsion between subnetworks
pos = nx.spring_layout(G, k=0.8, iterations=5)

# Map parent and product IDs to m/z values
parent_mz_map = {row["ID"]: row["mz"] for _, row in parent_df.iterrows()}
product_mz_map = {row["ID"]: row["mz"] for _, row in product_df.iterrows()}

# Get the m/z values for connected nodes
node_mz = []
for node in connected_nodes:
    if node in parent_mz_map:
        node_mz.append(parent_mz_map[node])
    elif node in product_mz_map:
        node_mz.append(product_mz_map[node])

node_sizes = [mz * 1 for mz in node_mz]  # Adjust size factor as needed

# Plot the network with nodes, edges, and labels
nx.draw_networkx_edges(G, pos, width=[G[u][v]["weight"] * 2 for u, v in G.edges], edge_color="grey")
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
nx.draw_networkx_labels(G, pos)

# Save the plot
plt.savefig('network.png', dpi=1000)
plt.show()
