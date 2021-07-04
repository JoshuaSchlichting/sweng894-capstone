from typing import Optional, List

from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId

from core.abstract_data_access_layer import AbstractDataAccessLayer


class UserNotFoundError(Exception):
    pass


class MongoDbApi(AbstractDataAccessLayer):

    def __init__(self, mongo_client: MongoClient) -> None:
        self._mongo_client = mongo_client
        self._db = self._mongo_client.vote_system
    
    def create_user(self, username: str, password: Optional[str]=None) -> str:
        id = self._db.users.insert_one({"username": username, "password": password, "type": "standard_account"}).inserted_id
        return str(id)

    def cast_vote(self, user_id: int, election_id: int, ranked_candidate_list: List[int]) -> int:
        return self._db.votes.insert_one(dict(user_id=user_id, election_id=election_id, ranked_candidate_list=ranked_candidate_list)).inserted_id
    
    def get_vote(self, id: int) -> dict:
        return self._db.votes.find_one({}, {"_id": id})

    def create_candidate(self, username: str) -> str:
        id = self._db.users.find_one_and_update(
            filter={"username": username},
            update={'$setOnInsert': {"username": username, "isCandidate": True}},
            upsert=True, new=True
        ).get("_id")
        return str(id)
    
    def create_election(self, election_name: str) -> int:
        id = self._db.elections.insert_one({"election_name": election_name}).inserted_id
        return str(id)
    
    def add_candidate_to_election(self, election_id: str, candidate_id: str) -> dict:
        elections = self._db.elections
        election = elections.find_one_and_update(
            {"_id": ObjectId(election_id)},
            {'$push': {"candidates": candidate_id}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        self._replace_id_with_str(election)
        return election

    def get_election(self, id: int) -> dict:
        election = self._db.elections.find_one({"_id": ObjectId(id)})
        self._replace_id_with_str(election)
        return election
    
    def get_user_info_by_id(self, user_id: int) -> dict:
        users_collection = self._db.users
        user_info = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_info:
            self._replace_id_with_str(user_info)
        else:
            raise UserNotFoundError(f"Database returned NULL when querying user '{user_id}'")
        return user_info
    
    def get_user_info_by_name(self, username: str) -> dict:
        user_info = self._db.users.find_one({"username": username})
        if user_info:
            self._replace_id_with_str(user_info)
        else:
            raise UserNotFoundError(f"Database returned NULL when searching for '{username}'")
        return user_info
    
    def get_user_is_valid(self, username: str, password: str) -> bool:
        user_info = self._db.users.find_one({"username": username, "password": password})
        return True if user_info else False

    def _replace_id_with_str(self, mongo_object: dict):
        """Replaces the mongo _id with a string value named 'id'

        Arguments:
            mongo_object: dict - This is a dictionary expected to contain an
              instance of a MongoDB ObjectId with the key "_id"

        Return:
            None - Python dictionaries are mutable, just like lists. With that, this
                   method returns nothing, while modifying the mongo_object passed in.
        """
        mongo_object["id"] = str(mongo_object.pop("_id"))
 
def create_mongo_api(host: str, port: int, username: str=None, password: str=None) -> MongoDbApi:
    client = MongoClient(host=host, port=port, username=username, password=password)
    return MongoDbApi(mongo_client=client)
