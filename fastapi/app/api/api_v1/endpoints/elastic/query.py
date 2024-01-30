from .dict import gettype
from .querystring import basicquery, nestedquery, rangequery, wildcardquery


def createquery(params):
    q = {}
    q["bool"] = {}
    q["bool"]["must"] = []
    for i in params:
        if gettype(i) == 1:
            q = basicquery(q, i, params[i])
        elif gettype(i) == 3:
            elem = i.split(".")
            q = nestedquery(q, elem[0], elem[1], params[i].split(","))
        elif gettype(i) == 4:
            values = params[i].split(",")
            q = rangequery(q, values[0], values[1], i)
    return q
