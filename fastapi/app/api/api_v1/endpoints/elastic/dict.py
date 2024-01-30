ejdict = {
    "businessdatefrom": "business_date",
    "businessdateto": "business_date",
    "status": "status",
    "transactiontype": "entry_details.transaction_type",
    "cashbox": "cashbox",
    "branch": "branch",
    "bank": "bank",
    "channel": "channel",
    "teller": "teller",
    "transaction_id": "transaction_id",
}

query_type_dict = {"normal": 1, "wildcard": 2, "nested": 3, "range": 4}


def gettype(type):
    normal = [
        "status",
        "cashbox",
        "branch",
        "bank",
        "channel",
        "teller",
        "transaction_id",
    ]
    wildcard = [""]
    nested = ["entry_details.transaction_type"]
    range = ["business_date"]
    if type in normal:
        return query_type_dict["normal"]
    elif type in wildcard:
        return query_type_dict["wildcard"]
    elif type in range:
        return query_type_dict["range"]
    elif type in nested:
        return query_type_dict["nested"]


def getsearchstring(req, search):
    for i in req:
        if ejdict[i] in search:
            if "from" in i:
                search[ejdict[i]] = req[i] + "," + search[ejdict[i]]
            else:
                search[ejdict[i]] = search[ejdict[i]] + "," + req[i]
        else:
            search[ejdict[i]] = req[i]
    return search
