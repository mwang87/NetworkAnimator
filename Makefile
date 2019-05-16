test:
	python ./networkx_test.py --inputGraphml data/test.graphml --output ./output/ --columns "precursor mass" "G1"

mauricio_test:
	python ./networkx_test.py --inputGraphml data/mauricio.graphml --component "50" --output ./output/ --columns "GNPSGROUP:L" "GNPSGROUP:A1" "GNPSGROUP:B1" "GNPSGROUP:C1" "GNPSGROUP:D1" "GNPSGROUP:TT" "GNPSGROUP:TM" "GNPSGROUP:TB" 
	ffmpeg -framerate 2 -i ./output/%03d.png output/output.mp4
	ffmpeg -i output/output.mp4 -vf fps=2,scale=320:-1:flags=lanczos,palettegen palette.png
	ffmpeg -i output/output.mp4 -i palette.png -filter_complex "fps=2,scale=1200:-1:flags=lanczos[x];[x][1:v]paletteuse" output/output.gif


NODE=1663

mauricio_node:
	rm output/*
	python ./networkx_test.py --inputGraphml data/mauricio.graphml --node $(NODE) --output ./output/ --columns "GNPSGROUP:L" "GNPSGROUP:A1" "GNPSGROUP:B1" "GNPSGROUP:C1" "GNPSGROUP:D1" "GNPSGROUP:TT" "GNPSGROUP:TM" "GNPSGROUP:TB" 
	ffmpeg -y -framerate 2 -i ./output/%03d.png output/output.mp4
	ffmpeg -y -i output/output.mp4 -vf fps=2,scale=320:-1:flags=lanczos,palettegen output/palette.png
	ffmpeg -y -i output/output.mp4 -i output/palette.png -filter_complex "fps=2,scale=1200:-1:flags=lanczos[x];[x][1:v]paletteuse" output/$(NODE).gif