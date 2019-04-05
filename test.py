"""Lets try to get all visual properties and save to json files ourselves"""

from py2cytoscape import cyrest
from py2cytoscape.data.cyrest_client import CyRestClient
import sys
import json

cy  = CyRestClient()


#cytoscape=cyrest.cyclient()
#cytoscape.version()

#full_style_json = cytoscape.styles.getStyleFull(sys.argv[1], verbose=True).json()

#open(sys.argv[2], "w").write(json.dumps(full_style_json, indent=4))



#cytoscape.vizmap.mapVisualProperty(visualProperty="", mappingType="", mappingColumn="")

#groups = ["GNPSGROUP:fungal culture", "GNPSGROUP:plant"]
