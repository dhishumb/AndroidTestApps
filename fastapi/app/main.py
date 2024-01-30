from fastapi import FastAPI
from fastapi.params import Query
from .api.api_v1.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

loggingfile = os.path.join(os.getcwd(), "app", "logging.conf")
logging.config.fileConfig(loggingfile, disable_existing_loggers=True)
logger = logging.getLogger(__name__)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    logger.info("mylog")
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/api/v1")
