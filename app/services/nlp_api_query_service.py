import json
from urllib.parse import quote
import requests


class NLPAPIQueryService:

    def __init__(self, *, diffbot_token):
        self.TOKEN = diffbot_token
        self.FIELDS = 'entities, facts'
        self.HOST = 'nl.diffbot.com'
        self.PORT = '80'

    def get_request(self, *, payload):
        # why does post no longer work? i have no clue.
        res = requests.post("https://{}/v1/?fields={}&token={}".format(self.HOST, self.FIELDS, self.TOKEN),
                            json=payload)
        # res = requests.post("http://{}/v1/?fields={}&token={}&content={}".format(
        #     self.HOST, self.FIELDS, self.TOKEN, payload['content']))
        # res = requests.get(res.text)
        return res.json()

    def get_request_for_str(self, *, input_str: str):
        payload = {
            'content': input_str,
            'lang': 'en',
            'format': 'plain text'
        }
        return self.get_request(payload=payload)

    def get_central_node_and_facts(self, data):
        max_facts = 0
        central_node = None
        key_facts = []
        if not data['entities']:
            # print('no central node detected')
            return None, None
        for ent in data['entities']:
            # print(ent['name'])
            fact_count = 0
            rel_facts = []
            for fact in data['facts']:
                fact_target_uri = fact['entity'].get('diffbotUri', '')
                if fact_target_uri and fact_target_uri == ent.get('diffbotUri', ''):
                    fact_count += 1
                    # print(fact)
                    rel_facts.append((fact['property']['diffbotUri'][41:], fact['value']['name'].lower()))
                    # print(fact)
                    # print(fact['property']['diffbotUri'][41:], fact['value']['name'])
            if fact_count > max_facts:
                max_facts = fact_count
                central_node = ent
                key_facts = rel_facts
        # print("-----")
        if not ent:
            # print('no central node detected')
            return None, None
        return central_node, key_facts
