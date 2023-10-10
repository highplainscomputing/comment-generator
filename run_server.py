#!/usr/bin/env python
"""Runs server API for end-to-end Comment Generator pipeline.

TODO: Refactor the Serialization and Deserialization part.
"""
import os
from typing import Dict, Tuple
from fastapi import FastAPI, Form, status, HTTPException
from fastapi.encoders import jsonable_encoder
from comment_generator import logger

from fastapi.responses import JSONResponse

from comment_generator.utils.parse_config import parse_config
from comment_generator.pipeline import Pipeline
from comment_generator.utils.db_utils import initialize_mongodb_instance, comment_deserializer

# Initialize app for fast api.
app = FastAPI()

# Config path for Pipeline
CONFIG = os.getenv('CONFIG', 'config.yaml')
CFG = parse_config(config_path=CONFIG)

# Initialize Pipeline.
PIPELINE = Pipeline.from_config(CFG)

# Initialize MongoDB Client and database
MONGO_CLIENT, MONGO_DB, COLLECTION_NAME = initialize_mongodb_instance(config=CFG)


@app.get("/health")
def health() -> Tuple[Dict, int]:
    """Checks Server Status"""
    if PIPELINE is None:
        return {"message": "Initializing Server"}, 503
    return {'message': 'Server is Running'}, 200


@app.on_event("startup")
async def startup_db_client():
    # TODO: use fast api event decorator for initializing database client
    app.mongodb_client = MONGO_CLIENT
    app.mongodb = MONGO_DB


@app.on_event("shutdown")
async def shutdown_db_client():
    # TODO: use fast api event decorator for closing database client
    app.mongodb_client.close()


@app.post('/generate')
async def generate(input_text: str = Form(...)) -> JSONResponse:
    """Performs Classification , NER on given text data and Generate Comment Generator.
        Returns:
            Response with content-type header 'application/json' with the following content:
            {
            'entities': [{'field': ['entity']}],
             'category': 'politics',
             'comment': 'this comment looks sample'
             }
        """
    result = PIPELINE.apply(post=input_text)
    json_object = jsonable_encoder(result)
    inserted_object = await MONGO_DB[COLLECTION_NAME].insert_one(json_object)
    logger.info('Output Object With Id {} Successfully Added to collection.'.format(inserted_object.inserted_id))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@app.get('/view')
async def view() -> list:
    list_of_comments = []
    async for comment_object in MONGO_DB[COLLECTION_NAME].find():
        deserialized_object = comment_deserializer(comment_object)
        list_of_comments.append(deserialized_object)
    if list_of_comments:
        logger.info('All Objects Successfully Retrieved.')
        return list_of_comments
    raise HTTPException(status_code=404, detail=f"No Comments Found.")
