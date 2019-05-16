test:
	python ./networkx_test.py --inputGraphml data/test.graphml --output ./output/ --columns "precursor mass" "G1"

mauricio:
	python ./networkx_test.py --inputGraphml data/network.graphml --component "50" --output ./output/ --columns "GNPSGROUP:plant" "GNPSGROUP:fungal culture"