import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import pandas as pd
import json
from PIL import Image


def get_component(G, component_number=None, node_index=None):
    nodes_list = list(G.nodes(data=True))

    component_header = "componentindex"

    if component_number != None:
        component_nodes = [node[0] for node in nodes_list if int(node[1][component_header]) == int(component_number)]
    if node_index != None:
        node_search = [node for node in nodes_list if int(node[0]) == int(node_index)][0]
        component_number = node_search[1][component_header]
        component_nodes = [node[0] for node in nodes_list if int(node[1][component_header]) == int(component_number)]

    print("Found", len(component_nodes))
    
    sub_G = G.subgraph(component_nodes)

    return sub_G, nx.spring_layout(sub_G, seed=0, k=0.75)

def get_all_component_list(G):
    nodes_list = list(G.nodes(data=True))
    component_header = "componentindex"
    component_list = [int(node[1][component_header]) for node in nodes_list if int(node[1][component_header]) != -1]

    unique_components = list(set(component_list))
    component_counts = [component_list.count(component) for component in unique_components]

    return zip(unique_components, component_counts)

def draw_component(sub_G, positions, draw_columns=["precursor mass"], output_directory="output", outputfileprefix=""):
    nodes_list = list(sub_G.nodes(data=True))

    for node in nodes_list:
        max_node_size = max([node[1][size_column] for size_column in draw_columns])
        min_node_size = min([node[1][size_column] for size_column in draw_columns])

        min_size = 50
        max_size = 500

        for size_column in draw_columns:
            component_size = node[1][size_column]

            xp = [min_node_size, max_node_size]
            fp = [min_size, max_size]
        
            new_component_size = np.interp([component_size], xp, fp)[0]
            node[1][size_column] = new_component_size

    
    for i, size_column in enumerate(draw_columns):
        component_sizes = [node[1][size_column] for node in nodes_list]

        node_labels = {}
        for node in nodes_list:
            #node_labels[node[0]] = ""
            node_labels[node[0]] = node[1]["precursor mass"]

        plt.figure(1,figsize=(12,12))
        nx.draw_networkx(sub_G, node_size=component_sizes, pos=positions, labels=node_labels)

        #Trying edge labels
        #edge_labels = nx.get_edge_attributes(sub_G,'mass_difference')
        #nx.draw_networkx_edge_labels(G, pos=positions, edge_labels = edge_labels)

        output_filename = os.path.join(output_directory, ('%03d' % i) + "_" + size_column + ".png")
        output_filename2 = os.path.join(output_directory, outputfileprefix + ('%03d' % i) + ".png")
        plt.title("Index %i - Group %s" % (i, size_column))

        #plt.savefig(output_filename)
        plt.savefig(output_filename2)
        plt.clf()

    return None


def merge_images(input_list, output_filename, CANVAS_WIDTH=5):
    ORIGINAL_WIDTH = 1200
    ORIGINAL_HEIGHT = 1200

    NEW_HEIGHT = ORIGINAL_HEIGHT * int((len(input_list) + 1)/CANVAS_WIDTH)
    NEW_WIDTH = ORIGINAL_WIDTH * CANVAS_WIDTH
    new_im = Image.new('RGB', (NEW_WIDTH, NEW_HEIGHT))

    for i, elem in enumerate(input_list):
        im=Image.open(elem)
        new_im.paste(im, ( (i % CANVAS_WIDTH) * ORIGINAL_WIDTH, int(i/CANVAS_WIDTH) * ORIGINAL_HEIGHT))
    new_im.save(output_filename)