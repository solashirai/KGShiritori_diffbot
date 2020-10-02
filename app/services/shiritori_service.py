from app.services.utils import *

class ShiritoriService:

    def __init__(self):
        self.seen_entities = []
        self.used_sentences = []
        self.seen_names = set()
        self.used_facts = set()
        self.previous_entity = None

    def clear(self):
        self.seen_entities = []
        self.used_sentences = []
        self.seen_names = set()
        self.used_facts = set()
        self.previous_entity = None

    def update_previous_entity_fact(self, *, entity, fact, input_str):
        self.seen_entities.append(entity)
        self.used_sentences.append(input_str)
        self.seen_names.add(entity['name'])
        if fact:
            self.used_facts.add(fact)
        self.previous_entity = entity

    def validate_next_step(self, entity, facts):
        print(self.seen_names)
        if entity['name'] in self.seen_names:
            yield False, -1
            return
        bad_candidates = []
        for fact in facts:
            match_in_previous = get_property_from_string(self.previous_entity, fact[0])
            # print(fact[0], '---', match_in_previous)
            if isinstance(match_in_previous, str):
                if match_in_previous.lower() == fact[1].lower():
                    if fact in self.used_facts:
                        bad_candidates.append(fact)
                    else:
                        yield True, fact
            elif isinstance(match_in_previous, list):
                for item in match_in_previous:
                    if isinstance(item, str):
                        if item.lower() == fact[1].lower():
                            if fact in self.used_facts:
                                bad_candidates.append(fact)
                            else:
                                yield True, fact
                    elif isinstance(item, dict):
                        path = search_path_to_name_value(item, fact[1].lower())
                        # print(path)
                        if path:
                            if fact in self.used_facts:
                                bad_candidates.append(fact)
                            else:
                                yield True, fact
            elif isinstance(match_in_previous, dict):
                path = search_path_to_name_value(match_in_previous, fact[1].lower())
                # print(path)
                if path:
                    if fact in self.used_facts:
                        bad_candidates.append(fact)
                    else:
                        yield True, fact
        for bc in bad_candidates:
            yield False, bad_candidates
        # yield False, 0

    def validate_real_fact(self, entity, fact):
        match_in_previous = get_property_from_string(entity, fact[0])
        # print(fact[0], '---', match_in_previous)
        if isinstance(match_in_previous, str):
            if match_in_previous.lower() == fact[1].lower():
                return True, fact
        elif isinstance(match_in_previous, list):
            for item in match_in_previous:
                if isinstance(item, str):
                    if item.lower() == fact[1].lower():
                        return True, fact
                elif isinstance(item, dict):
                    path = search_path_to_name_value(item, fact[1].lower())
                    if path:
                        return True
        elif isinstance(match_in_previous, dict):
            path = search_path_to_name_value(match_in_previous, fact[1].lower())
            # print(path)
            if path:
                return True
        return False
