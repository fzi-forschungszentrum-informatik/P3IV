import networkx as nx
import os
from matplotlib import pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def plot_roadmap(Graph, colormap, terminal_nodes, binary_combination, save_dir, header=""):

    # Create a directory for the given binary combination
    if os.path.isdir(save_dir) == False:
        os.makedirs(save_dir)

    # Create a colormap
    # http://stackoverflow.com/questions/13517614/draw-different-color-for-nodes-in-networkx-based-on-their-node-value
    values = [colormap.get(node, 0.25) for node in Graph.nodes()]

    pos = graphviz_layout(Graph, prog="dot")

    nx.draw(Graph, pos, arrows=True, node_size=1200, node_shape="o", node_color=values, edge_color="k")

    node_ids = str()
    for n in terminal_nodes:
        if len(node_ids) == 0:
            node_ids = node_ids + " " + n._id
        else:
            node_ids = node_ids + ", " + n._id

    text = "Terminal node(s): " + node_ids
    plt.annotate(text, xy=(0.05, 0.95), xycoords="axes fraction")

    plt.savefig(save_dir + "Roadmap" + " " + binary_combination + " " + header + ".png")
    plt.close()
