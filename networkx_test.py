import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import pandas as pd
import json

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


def draw_component(sub_G, positions, draw_columns=["precursor mass"], output_directory="output"):
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
        output_filename2 = os.path.join(output_directory, ('%03d' % i) + ".png")
        plt.title("%i %s" % (i, size_column))

        #plt.savefig(output_filename)
        plt.savefig(output_filename2)
        plt.clf()

    return None


    nodes_list = list(sub_G.nodes(data=True))
    component_sizes = [node[1][size_column] for node in nodes_list]

    #Formatting size
    max_value = max(component_sizes)
    min_value = min(component_sizes)

    min_size = 1
    max_size = 50

    xp = [min_value, max_value]
    fp = [min_size, max_size]

    component_sizes = np.interp(component_sizes, xp, fp)

    print(component_sizes)

    limits=plt.axis('off') 
    plt.figure(1,figsize=(12,12)) 
    nx.draw(sub_G, node_color=component_sizes, pos=positions)
    limits=plt.axis('off') 
    plt.savefig(output_filename)
    plt.clf()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--inputGraphml', default="data/test.graphml")
parser.add_argument('--output_folder', default="output")
parser.add_argument('--component', default=None)
parser.add_argument('--node', default=None)
parser.add_argument('--columns', type=str, nargs='+', default=None)
parser.add_argument('--columnsfile', type=str, default=None)

args = parser.parse_args()

print(args)

columns = []
if args.columns != None:
    columnns = args.columns
if args.columnsfile != None:
    columns = list(pd.read_csv(args.columnsfile)["groups"])
    print(columns)


G = nx.read_graphml(args.inputGraphml)
sub_G, positions = get_component(G, component_number=args.component, node_index=args.node)

"""Checking columns are all present"""
nodes_list = list(sub_G.nodes(data=True))
for column in columns:
    if not column in nodes_list[0][1]:
        print(column, "missing")
draw_component(sub_G, positions, draw_columns=columns, output_directory=args.output_folder)

# for i, column in enumerate(args.columns):
#     output_filename = os.path.join(args.output_folder, args.component + "_" + str(i) + "_" + column + ".png")
#     draw_component(sub_G, positions, size_column=column, output_filename=output_filename)






