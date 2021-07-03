from typing import Optional, List

from pymongo import MongoClient
from bson.objectid import ObjectId

from core.abstract_data_access_layer import AbstractDataAccessLayer


class MongoDbApi(AbstractDataAccessLayer):

    def __init__(self, mongo_client: MongoClient) -> None:
        self._mongo_client = mongo_client
        self._db = self._mongo_client.vote_system
    
    def create_user(self, username: str, password: Optional[str]=None) -> str:
        id = self._db.users.insert_one({"username": username, "password": password}).inserted_id
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
    
    def create_election(self, election_name: str, candidate_list: List[int]) -> int:
        id = self._db.elections.insert_one({"election_name": election_name, "candidate_list": candidate_list}).inserted_id
        return str(id)

    def get_election(self, id: int) -> dict:
        return self._db.elections.find_one({"_id": ObjectId(id)})
    
    def get_user_info_by_id(self, user_id: int) -> dict:
        return super().get_user_info_by_id()
    
    def get_user_info_by_name(self, username: str) -> dict:
        user_info = self._db.users.find_one({"username": username})
        user_info["id"] = user_info.pop("_id")
        return user_info
    
    def get_user_is_valid(self, username: str, password: str) -> bool:
        user_info = self._db.users.find_one({"username": username, "password": password})
        return True if user_info else False
 
def create_mongo_api(host: str, port: int, username: str=None, password: str=None) -> MongoDbApi:
    client = MongoClient(host=host, port=port, username=username, password=password)
    return MongoDbApi(mongo_client=client)