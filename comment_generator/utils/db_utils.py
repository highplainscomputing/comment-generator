"""
Utility Functions for async database operations

TODO: Improving the CRUD Operations utility functions
"""
import os
from typing import Dict, Any
import asyncio
from comment_generator import logger
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder


def comment_deserializer(comment_object) -> dict:
    """Helper function to decode Comment Object to general dict"""
    return {
        "id": str(comment_object["_id"]),
        "category": comment_object["category"],
        "entities": comment_object["entities"],
        "comment": comment_object["comment"]
    }


def asyncio_process(db_query):
    """decorator for async database operation"""

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(db_query(*args, **kwargs))

    return wrapper


@asyncio_process
async def create_collection(async_db, collection_name):
    list_of_collection = await async_db.list_collection_names()
    if collection_name not in list_of_collection:
        async_db.create_collection(collection_name)


def initialize_mongodb_instance(config: Dict[str, Any]) -> (AsyncIOMotorClient, Any, str):
    """
    Initialize a MongoDB Async Instance using Motor Client and Creates a collection for insertion of Json Objects.

    Returns:
        AsyncIOMotorClient, Doc Collection Name

    """

    db_url = os.getenv('DB_URL', '')
    if not db_url:
        db_config = config['database']['no_sql']
        user = db_config.get('user', 'sibtain')
        host = db_config.get('host', '0.0.0.0')
        port = db_config.get('port', '27017')
        db_url = 'mongodb://{}:{}/{}'.format(host, port, user)
    mongodb_async_client = AsyncIOMotorClient(db_url)
    collection_name = config['database']['no_sql'].get('collection', 'comments')
    db_name = config['database']['no_sql'].get('db_name', 'aiDB')
    async_db = mongodb_async_client[db_name]
    return mongodb_async_client, async_db, collection_name


@asyncio_process
async def insert_record(output_json: Dict[str, Any], mongo_client: AsyncIOMotorClient, collection_name: str):
    json_object = jsonable_encoder(output_json)
    inserted_object = await mongo_client[collection_name].insert_one(json_object)
    logger.info(
        'Comments on Post With Id {} Successfully Added to Collection'.format(inserted_object.inserted_id))
    return inserted_object.inserted_id


@asyncio_process
async def view_records(mongo_client: AsyncIOMotorClient, collection_name: str) -> list:
    list_of_comments = await mongo_client[collection_name].find().to_list(1000)
    logger.info(
        'Comments Retrieved Successfully')
    return list_of_comments
