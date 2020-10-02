IGNORE_TERMS = {
    'gender', 'importance', 'origin', 'profileChangeProbability', 'type', 'crawlTimestamp','types','nbIncomingEdges',
    'eyeColor', 'languages', 'isAcquired','isDissolved','isNonprofit','isPublic',
    'country', 'url', 'image', 'origins', 'from', 'to',
    'summary','latitude', 'longitude','precision','allNames','logo', 'nbOrigins',
    "description", 'allDescriptions', 'recordId', 'diffbotUri', 'targetDiffbotUri',
    'allOriginalHashes', 'allUris', 'surfaceForm', 'allIds_DiffbotUsage', 'address', 'position', "id",
    'height', 'weight',
    'str'
}


def compare_dictionaries(dict_1, dict_2, updating_set, path=""):
    """Compare two dictionaries recursively to find non mathcing elements

    Args:
        dict_1: dictionary 1
        dict_2: dictionary 2

    Returns:

    """
    err = ''
    key_err = ''
    value_err = ''
    old_path = path
    for k in dict_1:
        path = old_path + "%s." % k
        if k in IGNORE_TERMS or isinstance(dict_1[k], int) or isinstance(dict_1[k], bool):
            continue
        if k in dict_2:
            if isinstance(dict_1[k], dict) and isinstance(dict_2[k], dict):
                compare_dictionaries(dict_1[k], dict_2[k], updating_set, path)
            elif isinstance(dict_1[k], list) and isinstance(dict_2[k], list):
                if len(dict_1[k]) == 0 or len(dict_2[k]) == 0:
                    continue
                if isinstance(dict_1[k][0], dict) and isinstance(dict_2[k][0], dict):
                    for subdict_1 in dict_1[k]:
                        for subdict_2 in dict_2[k]:
                            compare_dictionaries(subdict_1, subdict_2, updating_set, path)
                else:
                    for item in dict_1[k]:
                        if item in dict_2[k]:
                            if item != "" and item != "null":
                                updating_set.add(path[:-1] + ":" + f'"{item}"')

            else:
                if dict_1[k] == dict_2[k]:
                    if dict_1[k] != "" and dict_1[k] != "null":
                        updating_set.add(path[:-1] + ":" + f'"{dict_1[k]}"')


def get_all_fields(input_dict, output_list, path=""):
    old_path = path
    for k in input_dict:
        path = old_path + "%s." % k
        if k in IGNORE_TERMS or isinstance(input_dict[k], int) or isinstance(input_dict[k], bool):
            continue
        if isinstance(input_dict[k], dict):
            get_all_fields(input_dict[k], output_list, path)
        elif isinstance(input_dict[k], list):
            if len(input_dict[k]) == 0:
                continue
            if isinstance(input_dict[k][0], dict):
                for subdict_1 in input_dict[k]:
                    get_all_fields(subdict_1, output_list, path)
            else:
                for item in input_dict[k]:
                    output_list.append(path[:-1]+":"+f'"{item}"')
        else:
            output_list.append(path[:-1]+":"+f'"{input_dict[k]}"')

def get_property_from_string(entity, str='', parts=[]):
    # print(str, parts, entity)
    if not parts:
        parts = str.split(".")
    if not parts:
        return None
    output_val = entity
    final_outputs = []
    for ind, part in enumerate(parts):
        if part in IGNORE_TERMS:
            return []
        output_val = output_val.get(part, {})
        if isinstance(output_val, list):
            # print("!", str, " ", part, "---", parts[ind+1:])
            # for item in output_val:
            #     print(item)
            for item in output_val:
                if ind+1 < len(parts):
                    final_outputs.append(get_property_from_string(item, str='', parts=parts[ind+1:]))
                else:
                    final_outputs.append(item)
            # print(final_outputs)
            return final_outputs
    return output_val

def search_path_to_name_value(content_dict, target_val, old_path=''):
    paths = []
    for k in content_dict:
        path = old_path + "%s." % k
        if k in IGNORE_TERMS or isinstance(content_dict[k], int) or isinstance(content_dict[k], bool):
            continue
        if isinstance(content_dict[k], dict):
            new_paths = search_path_to_name_value(content_dict[k], target_val, old_path=path)
            for np in new_paths:
                paths.append(np)
        elif isinstance(content_dict[k], list):
            if len(content_dict[k]) == 0:
                continue
            if isinstance(content_dict[k][0], dict):
                for subdict in content_dict[k]:
                    new_paths = search_path_to_name_value(subdict, target_val, old_path=path)
                    for np in new_paths:
                        paths.append(np)
            else:
                for item in content_dict[k]:
                    if item != "" and item != "null" and item.lower() == target_val:
                        paths.append(path[:-1])

        else:
            if content_dict[k].lower() == target_val:
                paths.append(path[:-1])
    return paths
