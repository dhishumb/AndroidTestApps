from fastapi import APIRouter, Depends
from pydantic import BaseModel
from kubernetes import client, config
from typing import Optional
from kubernetes.client.rest import ApiException
import os
import json

router = APIRouter()

envdict = {'dev1':'rancher.conf', 'dev2':'rancher.conf', 'dev3':'rancher.conf', 'it1':'rancher.conf', 'it2':'rancher.conf', 'it3':'rancher.conf', 'uat1':'rancher.conf', 'uat2':'rancher.conf', 'uat3':'rancher.conf', 'uatp-cbc':'rancher-uatp-cbc.conf'}


class EnvModel(BaseModel):
    env: str
    namespace: Optional[str]
    podname: Optional[str]

@router.post("/getnamespace")
async def get_namespace(env: EnvModel):    
    conffile: str = envdict[env.env]
    confpath = os.path.join(os.getcwd(),'app','kubeconf', conffile)
    config.load_kube_config(confpath)
    v1 = client.CoreV1Api()
    ret = v1.list_namespace()
    namespace = list()
    stringtosearch = env.env.split('-')[0]
    for i in ret.items:
        if ('common-tran' in i.metadata.name and stringtosearch in i.metadata.name):
            namespace.append(i.metadata.name)
    resp = {
        "pods": namespace
    }
    return resp

@router.post("/getpods")
async def get_pods(env: EnvModel):    
    conffile: str = envdict[env.env]
    confpath = os.path.join(os.getcwd(),'app','kubeconf', conffile)
    config.load_kube_config(confpath)
    v1 = client.CoreV1Api()
    pods = list()
    ret_pods = v1.list_namespaced_pod(namespace= env.namespace, async_req = True)
    results = ret_pods.get()
    for r in results.items:
        pods.append(r.metadata.name)
    
    resp = {
        "pods": pods
    }
    return resp

@router.post("/getlogs")
async def get_logs(env: EnvModel):    
    conffile: str = envdict[env.env]
    confpath = os.path.join(os.getcwd(),'app','kubeconf', conffile)
    config.load_kube_config(confpath)
    v1 = client.CoreV1Api()
    ret_logs = list()
    try:
        api_response = v1.read_namespaced_pod_log(name=env.podname, namespace=env.namespace, pretty = True, tail_lines = 500)
        logs = api_response.split('\n') 
    except ApiException as e:
        print('error')
    for i in logs:
        if i:
            ret_logs.append(json.loads(i))
    resp = {
        "logs": ret_logs
    }
    return resp