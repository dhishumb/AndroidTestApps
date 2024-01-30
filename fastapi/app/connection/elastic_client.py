from fastapi import Depends 
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
import os

async def elastic_connect(config):
    certpath = config.elastic_certlocation
    context = create_ssl_context(cafile=certpath)
    host = os.environ.get('ELASTICSEARCH_HOST', config.elastic_hostname)
    port = os.environ.get('ELASTICSEARCH_PORT', config.elastic_port)
    username = os.environ.get('ELASTICSEARCH_USERNAME', config.elastic_username)
    password = os.environ.get('ELASTICSEARCH_PASSWORD', config.elastic_password)
    elasticconnectstring = 'https://' + username + ':' + password
    elasticconnectstring = elasticconnectstring + '@' + host + ':' + port

    es = Elasticsearch([elasticconnectstring], scheme="https", ssl_context=context, timeout=60)    
    return es