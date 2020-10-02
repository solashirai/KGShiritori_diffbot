import networkx as nx
from networkx.readwrite import json_graph
import json
import matplotlib.pyplot as plt
from app.services.utils import *


class VisualizationService:

    def fact_tup_to_readable(self, tup):
        if tup:
            return f"↓--- share {tup[1][0]} = {tup[1][1]}"
        else:
            return ''

    def status_string(self, res_code, input_str):
        if res_code == -1:
            return "The system failed to detect a main entity in your input!"
        elif res_code == 0:
            return "Success! Move to the next step!"
        elif res_code == 1:
            return "Some facts in your sentence matched, but they aren\'t present in the Diffbot KG."
        elif res_code == 2:
            return "You\'ve already used that person in this game!"
        elif res_code == 3:
            return "No facts in your sentence could connect to the previous node."
        elif res_code == 4:
            return "There was a fact match, but you\'ve already used that fact in this game!"
        elif res_code == 5:
            return "No facts were detected, or none of the facts were present in the Diffbot KG."
