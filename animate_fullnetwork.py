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
parser.add_argument('--columns', type=str, nargs='+', default=None)
parser.add_argument('--columnsfile', type=str, default=None)
args = parser.parse_args()

columns = []
if args.columns != None:
    columnns = args.columns
if args.columnsfile != None:
    columns = list(pd.read_csv(args.columnsfile)["groups"])

#All components
G = nx.read_graphml(args.inputGraphml)
component_list = animate_utils.get_all_component_list(G)

#Filter components to larger than size N
MIN_COMPONENT_SIZE = 10
component_list = [component[0] for component in component_list if component[1] > MIN_COMPONENT_SIZE]

component_list = component_list[:20]

for component in component_list:
    sub_G, positions = animate_utils.get_component(G, component_number=component)
    animate_utils.draw_component(sub_G, positions, draw_columns=columns, output_directory=args.output_folder, outputfileprefix=str(component) + ":")

#Merging all of them
for i, column in enumerate(columns):
    filenames = [os.path.join(args.output_folder, str(component) + ":" + ('%03d' % i) + ".png") for component in component_list]
    output_filename = os.path.join(args.output_folder, ('%03d' % i) + ".png")
    animate_utils.merge_images(filenames, output_filename)