from fastapi import APIRouter

from .endpoints.elastic import search
from .endpoints.kube import devops
from .endpoints.token import jwt
from .endpoints.cassandra import dboper

router = APIRouter()
router.include_router(search.router, prefix="/ej", tags=["EJ"])
router.include_router(devops.router, prefix="/devops", tags=["Logs"])
router.include_router(jwt.router, prefix="/token", tags=["JWT"])
router.include_router(dboper.router, prefix="/db", tags=["Cassandra"])