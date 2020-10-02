import json
from flask import Flask, request, abort, render_template
from app.services.app_driver import AppDriver
from app.services.visualization_service import VisualizationService
import sys


app = Flask(__name__)
TOKEN = '<insert your token here>'
shiritori = AppDriver(diffbot_token=TOKEN)
vis = VisualizationService()

@app.route("/")
def hello_world():
    firstname, firstimg = shiritori.setup_first_node()
    data = {
        'nodes': [{'id': firstname, 'label': firstname, 'image': firstimg}],
        'firstName': firstname
    }
    return render_template('home.html', data=data)


@app.route('/shiritori_reset', methods=['GET'])
def shiritori_reset():
    input_str = request.args.get('text')
    firstname, firstimg = shiritori.setup_first_node(query_str=input_str)
    data = {
        'newNode': {'id': firstname, 'label': firstname, 'image': firstimg},
        'firstName': firstname
    }
    return json.dumps(data)


@app.route('/shiritori_parse', methods=['GET'])
def shiritori_parse():
    input_str = request.args.get('text')
    if shiritori.ss.previous_entity:
        prev_entity_name = shiritori.ss.previous_entity['name']
    else:
        prev_entity_name = ""
    res_code, tup, new_entity_name, new_entity_img = shiritori.app_step(input_str=input_str)
    if tup:
        readable_success_relation = vis.fact_tup_to_readable(tup)
        status_str = vis.status_string(res_code, input_str)
    else:
        tup = ("", ("", ""))
        readable_success_relation = ""
        status_str = vis.status_string(res_code, input_str)
    # print(json.dumps({"successCode": res_code,
    #                    "entityContent": new_entity_name,
    #                    "entityImage": new_entity_img,
    #                    "previousEntity": prev_entity_name,
    #                    "relationContent": tup[1][1],
    #                    "relationContentReadable": readable_success_relation,
    #                   "statusString": "ree",
    #                     "relationType": tup[1][0]}))
    return json.dumps({"successCode": res_code,
                       "entityContent": new_entity_name,
                       "entityImage": new_entity_img,
                       "previousEntity": prev_entity_name,
                       "relationContent": tup[1][1],
                       "statusString": status_str,
                       "relationContentReadable": readable_success_relation,
                        "relationType": tup[1][0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=80)
