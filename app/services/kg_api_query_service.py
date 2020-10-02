import requests
from urllib.parse import quote
from app.services.utils import *


class KGAPIQueryService:

    def __init__(self, *, diffbot_token):
        #TODO: don't push this token
        self.TOKEN = diffbot_token
        self.TYPE = 'query'
        self.FROM = 0
        self.SIZE = 1
        self.HOST = 'https://kg.diffbot.com/kg/dql_endpoint'
        self.PORT = '80'

    def query_random_popular(self):
        query_str = quote('type:Person re:allUris:"dbpedia.+" re:allUris:"wikidata.+" re:allUris:"en.wikipedia.+" has:image sortBy:random')
        return self.get_request(payload=query_str)

    def get_request(self, *, payload):
        # print(f"{self.HOST}?type={self.TYPE}&token={self.TOKEN}&size={self.SIZE}&from={self.FROM}&query={payload}")
        res = requests.get(f"{self.HOST}?type={self.TYPE}&token={self.TOKEN}&size={self.SIZE}&from={self.FROM}&query={payload}")

        return res.json()

    def query_kg(self, *, query_str: str):
        query_str = quote(query_str)
        return self.get_request(payload=query_str)

    def create_query(self, *, type: str, fields_for_query: str, not_fields):
        not_str = [f'NOT({item})' for item in not_fields]
        not_str = " ".join(not_str)
        return f'type:{type} re:allUris:"dbpedia.+" re:allUris:"wikidata.+" re:allUris:"en.wikipedia.+" OR({fields_for_query}) {not_str} sortBy:random'

    def shiritori_queries(self, *, cn_type, previous_entity, used_properties, seen_entities):

        fields_list = []
        get_all_fields(previous_entity, fields_list)
        # print('asdf', len(fields_list))
        fields_list = set(fields_list) - used_properties
        # print("bbdf", len(fields_list))
        # fields_list = random.sample(fields_list, 5)
        fields_for_query = ", ".join(f"strict:{item}" for item in fields_list)
        create_query = self.create_query(type=cn_type, fields_for_query=fields_for_query, not_fields=used_properties)

        step_res = self.query_kg(query_str=create_query)
        # print(step_res)
        step_ent = step_res['data'][0]
        # print(step_ent['name'], '---', step_ent)
        # print()
        for ent in seen_entities:
            compare_dictionaries(ent, step_ent, used_properties)
        seen_entities.append(step_ent)
        return step_ent
