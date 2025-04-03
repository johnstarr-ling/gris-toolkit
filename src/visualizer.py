import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import argparse


###############################################################################
# Load arguments 
###############################################################################

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input_file', type=str,
                    default='./outputs/demo-2-distances.csv',
                    help='Input file (must have distances calculated).')

parser.add_argument('-o', '--output_folder', type=str,
                    default='./outputs/', 
                    help='Output folder location.')

parser.add_argument('-f', '--filename', type=str,
                    default='image',
                    help='Output file name.')

parser.add_argument('-t', '--title', type=str, 
                    default='Object Relationship Graph (distance~similarity)',
                    help='Title of output graph.')

parser.add_argument('-c', '--condition', type=str,
                    default='object',
                    help='Name of column that you want to visualize, along with its double (col, col_2).')

parser.add_argument('-g', '--graph_type', type=str,
                    nargs='+',
                    choices=['2D', '3D', '3D_static'],
                    default='3D')

args = parser.parse_args()

INPUT = args.input_file
TITLE = args.title 
FOLDER = args.output_folder
OUTPUT= args.filename
CONDITION=args.condition
GRAPHS=args.graph_type 



###############################################################################
# Visualization functions 
###############################################################################

def build_graph_from_df(df, condition=CONDITION):
    """Helper function to create a weighted undirected graph from a DataFrame."""
    G = nx.Graph()
    for _, row in df.iterrows():
        obj1, obj2, dist = row[f'{condition}'], row[f'{condition}_2'], row['distance']
        if pd.notna(obj1) and pd.notna(obj2) and pd.notna(dist):
            G.add_edge(obj1, obj2, weight=dist)
    return G


def graph_3d_animate(df, save_path=f'{FOLDER}/{OUTPUT}_3D.gif', title=TITLE):
    """Create a 3D animated rotation of the object graph and save as a GIF."""
    G = build_graph_from_df(df)
    pos_3d = nx.spring_layout(G, dim=3, weight='weight', seed=42)
    
    nodes = list(G.nodes())
    edges = list(G.edges())
    xyz = np.array([pos_3d[node] for node in nodes])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    def update(frame):
        ax.clear()
        ax.set_title(title, fontsize=14)
        ax.set_axis_off()
        ax.view_init(elev=20, azim=frame)

        # Draw nodes
        ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=300, c='skyblue', edgecolors='k')

        # Draw edges
        for u, v in edges:
            x = [pos_3d[u][0], pos_3d[v][0]]
            y = [pos_3d[u][1], pos_3d[v][1]]
            z = [pos_3d[u][2], pos_3d[v][2]]
            ax.plot(x, y, z, c='gray')

        # Node labels
        for i, node in enumerate(nodes):
            ax.text(*xyz[i], node, fontsize=10, ha='center', va='center')

    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=100)
    ani.save(save_path, writer=PillowWriter(fps=10))
    print(f"3D animation saved as '{save_path}'")


def graph_3d_static(df, save_path=f'{FOLDER}/{OUTPUT}_3D_static.pdf', title=TITLE):
    """Save a static 3D image of the object graph."""
    G = build_graph_from_df(df)
    pos_3d = nx.spring_layout(G, dim=3, weight='weight', seed=42)

    nodes = list(G.nodes())
    edges = list(G.edges())
    xyz = np.array([pos_3d[node] for node in nodes])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title, fontsize=14)
    ax.set_axis_off()
    ax.view_init(elev=20, azim=45)

    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=300, c='skyblue', edgecolors='k')

    for u, v in edges:
        x = [pos_3d[u][0], pos_3d[v][0]]
        y = [pos_3d[u][1], pos_3d[v][1]]
        z = [pos_3d[u][2], pos_3d[v][2]]
        ax.plot(x, y, z, c='gray')

    for i, node in enumerate(nodes):
        ax.text(*xyz[i], node, fontsize=10, ha='center', va='center')

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Static 3D graph saved as '{save_path}'")


def graph_2d_static(df, save_path=f'{FOLDER}/{OUTPUT}_2D.pdf', title=TITLE):
    """Draw and save a 2D layout of the object graph using inverse distance as force strength."""
    G = build_graph_from_df(df)

    # Set inverse weights for spring layout
    inv_weights = {(u, v): 1 / d['weight'] for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, inv_weights, 'inv_weight')

    pos = nx.spring_layout(G, weight='inv_weight', seed=42)

    plt.figure(figsize=(10,8))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000, edgecolors='k')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Show actual distances on edges
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"2D graph saved as '{save_path}'")



###############################################################################
# MAIN 
###############################################################################

if __name__ == '__main__':
    data = pd.read_csv(INPUT)

    if '3D' in GRAPHS:
        graph_3d_animate(data)
    
    if '3D_static' in GRAPHS:
        graph_3d_static(data)

    if '2D' in GRAPHS:
        graph_2d_static(data)


