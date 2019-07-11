# Network Animator  

Welcome to Network Animator

## Animating Components

To animate a component of a network, there are two ways to enter the information denoting the component:

by node

`python ./animate_component.py --inputGraphml $(QUERY_FILENAME) --node $(NODE) --output ./output/ --columnsfile $(COLUMNSFILENAME)`

by component

`python ./animate_component.py --inputGraphml $(QUERY_FILENAME) --component $(COMPONENT) --output ./output/ --columnsfile $(COLUMNSFILENAME)`


Additionally, to denote the groups to display as size throughout the animation, they can be entered on the commandline, or as a text file. This text file format is a single column with the header groups. 


## Animating Paired Metadata

## Animating Full Network