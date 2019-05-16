import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import pandas as pd

def get_component(G, component_number):
    nodes_list = list(G.nodes(data=True))

    print(nodes_list[0][1]["componentindex"])

    component_nodes = [node[0] for node in nodes_list if int(node[1]["componentindex"]) == int(component_number)]

    print(component_nodes)
    
    sub_G = G.subgraph(component_nodes)

    return sub_G, nx.spring_layout(sub_G, seed=0)


def draw_component(sub_G, positions, columns=["precursor mass"], output_directory="output"):
    nodes_list = list(sub_G.nodes(data=True))
    
    for node in nodes_list:
        max_node_size = max([node[1][size_column] for size_column in columns])
        min_node_size = min([node[1][size_column] for size_column in columns])

        min_size = 1
        max_size = 100

        for size_column in columns:
            component_size = node[1][size_column]

            xp = [min_node_size, max_node_size]
            fp = [min_size, max_size]
        
            new_component_size = np.interp([component_size], xp, fp)[0]
            node[1][size_column] = new_component_size

    
    for i, size_column in enumerate(columns):
        component_sizes = [node[1][size_column] for node in nodes_list]
        plt.figure(1,figsize=(12,12)) 
        nx.draw(sub_G, node_color=component_sizes, pos=positions)

        output_filename = os.path.join(output_directory, ('%03d' % i) + "_" + size_column + ".png")
        output_filename2 = os.path.join(output_directory, ('%03d' % i) + ".png")
        plt.savefig(output_filename)
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
parser.add_argument('--component', default="22")
parser.add_argument('--columns', type=str, nargs='+', default=["precursor mass"])

args = parser.parse_args()

print(args)

G = nx.read_graphml(args.inputGraphml)
sub_G, positions = get_component(G, args.component)

draw_component(sub_G, positions, columns=args.columns, output_directory=args.output_folder)

# for i, column in enumerate(args.columns):
#     output_filename = os.path.join(args.output_folder, args.component + "_" + str(i) + "_" + column + ".png")
#     draw_component(sub_G, positions, size_column=column, output_filename=output_filename)






