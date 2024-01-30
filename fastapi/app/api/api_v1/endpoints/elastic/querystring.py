def basicquery(q, element, element_value):
    temp = {"match": {element: element_value}}
    q["bool"]["must"].append(temp)
    return q


def rangequery(q, lower, upper, element):
    temp = {"range": {element: {"gte": lower, "lte": upper}}}
    q["bool"]["must"].append(temp)
    return q


def nestedquery(q, element_type, element_subtype, element_value):
    criteria = element_type + "." + element_subtype
    n = {}
    n["bool"] = {}
    n["bool"]["should"] = []
    for i in element_value:
        ne = {}
        ne["nested"] = {}
        ne["nested"]["path"] = element_type
        ne["nested"]["query"] = {}
        ne["nested"]["query"]["bool"] = {}
        ne["nested"]["query"]["bool"]["must"] = []
        item = {"match": {criteria: i}}
        ne["nested"]["query"]["bool"]["must"].append(item)
        n["bool"]["should"].append(ne)
    q["bool"]["must"].append(n)
    return q


def wildcardquery(q, element, element_value):
    temp = {"wildcard": {element: element_value}}
    q["bool"]["should"].append(temp)
    return q