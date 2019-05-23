import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import pandas as pd
import json
from PIL import Image
import animate_utils

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--inputGraphml', default="data/test.graphml")
parser.add_argument('--output_folder', default="output")
parser.add_argument('--component', default=None)
parser.add_argument('--node', default=None)
parser.add_argument('--columnsfile', type=str, default=None)
args = parser.parse_args()


columns_df = pd.read_csv(args.columnsfile, sep="\t")

print(columns_df)

columns1 = list(columns_df["groups1"])
columns2 = list(columns_df["groups2"])
    
G = nx.read_graphml(args.inputGraphml)
sub_G, positions = animate_utils.get_component(G, component_number=args.component, node_index=args.node)

animate_utils.draw_component(sub_G, positions, draw_columns=columns1, output_directory=args.output_folder, outputfileprefix="group1:")
animate_utils.draw_component(sub_G, positions, draw_columns=columns2, output_directory=args.output_folder, outputfileprefix="group2:")

#Merge Pairs of Molecules
for i, column in enumerate(columns1):
    filenames = [os.path.join(args.output_folder, "group1:" + ('%03d' % i) + ".png"), os.path.join(args.output_folder, "group2:" + ('%03d' % i) + ".png")]
    output_filename = os.path.join(args.output_folder, ('%03d' % i) + ".png")
    animate_utils.merge_images(filenames, output_filename, CANVAS_WIDTH=2)