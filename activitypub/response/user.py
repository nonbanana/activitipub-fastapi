from pydantic import BaseModel, Field
from typing import List

class PublicKey(BaseModel):
    id : str # "https://example.com/users/zampano#main-key",
    owner: str # "https://example.com/users/zampano",
    publicKeyPem: bytes
    # {
    #     "id": "https://example.com/users/zampano#main-key",
    #     "id": "https://example.com/users/zampano",
    #     : 
    # }

class UserResponse(BaseModel):
    at_context: List[str] = Field(["https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",], alias='@context')
    id: str # "https://example.com/users/nonbanana",
    inbox: str # "https://example.com/users/nonbanana/inbox",
    outbox: str # "https://example.com/users/nonbanana/outbox",
    type: str # "Person",
    name: str # "nonbanana",
    preferredUsername:str #"nonbanana",
    publicKey: PublicKey
    
    # def json(self, *args, **kwargs):
    #     return super().json(*args, **kwargs)
        