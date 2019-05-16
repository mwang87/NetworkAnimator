test:
	python ./networkx_test.py --inputGraphml data/test.graphml --output ./output/ --columns "precursor mass" "G1"

mauricio:
	python ./networkx_test.py --inputGraphml data/mauricio.graphml --component "50" --output ./output/ --columns "GNPSGROUP:plant" "GNPSGROUP:fungal culture"
	#ffmpeg -framerate 2 -i ./output/%03d.png output/output.gif
