from app.services.nlp_api_query_service import NLPAPIQueryService
from app.services.shiritori_service import ShiritoriService
from app.services.kg_api_query_service import KGAPIQueryService
import random


class AppDriver:

    def __init__(self, *, diffbot_token):
        self.ss = ShiritoriService()
        self.nlpqs = NLPAPIQueryService(diffbot_token=diffbot_token)
        self.kgqs = KGAPIQueryService(diffbot_token=diffbot_token)

    def setup_first_node(self, query_str=''):
        self.ss.clear()
        if query_str:
            res = self.nlpqs.get_request_for_str(input_str=query_str)
            central_node, key_facts = self.nlpqs.get_central_node_and_facts(data=res)
            if not central_node or not key_facts:
                ent = res['entities'][0]
                if not ent:
                    first_entity = self.kgqs.query_random_popular()
                else:
                    if not ent.get('diffbotUri', ''):
                        first_entity = self.kgqs.query_random_popular()
                    else:
                        cn_id = ent['diffbotUri'][27:]
                        first_entity = self.kgqs.query_kg(query_str=f"id:{cn_id}")
            else:
                cn_id = central_node['diffbotUri'][27:]
                first_entity = self.kgqs.query_kg(query_str=f"id:{cn_id}")
        else:
            first_entity = self.kgqs.query_random_popular()

        # print(first_entity)
        first_entity = first_entity['data'][0]
        self.ss.update_previous_entity_fact(entity=first_entity, fact=None, input_str='')
        return first_entity['name'], first_entity.get('image', '')

    def app_step(self, *, input_str):
        success = False
        return_code = None  # 0 - success, 1 - bad facts, 2 - already used person, 3 - no match, 4 - already used fact
        success_fact = None
        # print('input: ', input_str)

        res = self.nlpqs.get_request_for_str(input_str=input_str)
        # print('res: ', res)

        central_node, key_facts = self.nlpqs.get_central_node_and_facts(data=res)
        if not central_node or not key_facts:
            return -1, None, None, None

        # print(key_facts)

        if len(self.ss.seen_entities) == 0:
            cn_id = central_node['diffbotUri'][27:]
            res = self.kgqs.query_kg(query_str=f"id:{cn_id}")
            first_ent_from_kg = res['data'][0]  # assuming only 1 entity with this unique ID
            if first_ent_from_kg:
                self.ss.update_previous_entity_fact(entity=first_ent_from_kg, fact=None, input_str=input_str)
                return 0, None, first_ent_from_kg['name'], first_ent_from_kg.get('image', '')
            else:
                # print("Invalid or missing key node")
                return -1, None, None, None

        # print('prev: ', self.ss.previous_entity['name'])
        # print(list(self.ss.validate_next_step(central_node, key_facts)))


        valid_fact = list(self.ss.validate_next_step(central_node, key_facts))
        if any(tup[0]==1 for tup in valid_fact):
            cn_id = central_node['diffbotUri'][27:]
            res = self.kgqs.query_kg(query_str=f"id:{cn_id}")
            first_ent_from_kg = res['data'][0]
            for tup in valid_fact:
                if tup[1] and self.ss.validate_real_fact(first_ent_from_kg, tup[1]):
                    # print("Success!", tup)
                    self.ss.update_previous_entity_fact(entity=first_ent_from_kg, fact=tup[1], input_str=input_str)
                    success = True
                    return 0, tup, first_ent_from_kg['name'], first_ent_from_kg.get('image', '')
            if not success:
                # print("There were matching facts, but the facts were not reflected in the KG.")
                return 1, None, None, None
        else:
            if len(valid_fact) == 0:
                # print('There weren\'t any facts in your sentence that match with the previous node!')
                return 3, None, None, None
            elif all(tup[1] == -1 for tup in valid_fact):
                # print('That person has already been used in this game!')
                return 2, None, None, None
            elif all(tup[1] == 0 for tup in valid_fact):
                # print('There weren\'t any facts in your sentence that match with the previous node!')
                return 3, None, None, None
            else:
                # print('You already used facts that could match to the previous node!')
                return 4, None, None, None
