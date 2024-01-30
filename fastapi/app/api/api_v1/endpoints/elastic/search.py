from fastapi import APIRouter, Depends, Request
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBasic, HTTPBearer
from pydantic import BaseModel
from .....config import Settings, get_setting
from .....connection import elastic_client
from elasticsearch_dsl import Search, Q
from elasticsearch import helpers
from .dict import getsearchstring
from .query import createquery
import json
import ast

from app.api.api_v1.endpoints.elastic import query

router = APIRouter()
security = HTTPBearer()


class JournalIDSearch(BaseModel):
    journalid: str
    channel: str


@router.post("/getjournal")
async def search_journalid(
    journal: JournalIDSearch,
    config: Settings = Depends(get_setting),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    es = await elastic_client.elastic_connect(config)
    q = Q("match", channel=journal.channel)
    q1 = Q("match", _id=journal.journalid)
    s = Search(index=config.elastic_index).using(es).query(q).query(q1)
    total = s.count()
    if total > 0:
        result = list()
        for hit in s.scan():
            r = hit.to_dict()
            result.append(r)
        resp = {"results": r, "count": str(total)}
    else:
        resp = {"count": "0"}
    return resp


@router.post("/search")
async def searchej(request: Request, config: Settings = Depends(get_setting)):
    es = await elastic_client.elastic_connect(config)
    data = await request.json()
    search = {}
    search = getsearchstring(data, search)
    q = createquery(search)
    myquery = {}
    myquery["query"] = {}
    myquery["query"].update(q)
    results = helpers.scan(
        es,
        index=config.elastic_index,
        query=myquery,
        preserve_order=True,
        doc_type="transactions",
    )
    count = 0
    for item in results:
        print(item["_index"] + "," + item["_id"])
        count = count + 1
        if count > config.elastic_resultsize:
            break
    return await request.json()
