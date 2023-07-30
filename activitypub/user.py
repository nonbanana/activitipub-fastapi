from typing import List
import json
from fastapi import APIRouter, Depends, Query, HTTPException, status, Response, Request

from activitypub.response import UserResponse
from core.config import config
class ActivityPubResponse(Response):
    media_type = "application/activity+json"

user_router = APIRouter(default_response_class=ActivityPubResponse)

# public_key = (
#     b"-----BEGIN PUBLIC KEY-----\n"
#     b"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5iGLiV05JNeAHUhaDtZZ\n"
#     b"IfEJvFID28hMETdNUBUjM4X/QQGFQ2pNDNGoSLBuiliGnnMwQhjoB+FufM7CjAix\n"
#     b"fmQgNLWep1kdgZo21RL/068AV20Uuz0zwOIAL8/s9SrfSglK8NfIRzohdfwWQsmm\n"
#     b"KMtF0ohumxkvJY8ymU1/obO4HYJEpTnsM/QfsQ1qTuN94tMEh2oxowO6BJAps7vW\n"
#     b"6PGFZZesNW16/bUoKDHq0bTVYL/9v7lUgsk6D9UH6P++xDm027iwfSMjSQVat9Mm\n"
#     b"uxcEe9GSQ+rm4XHHqOtkyC0aWwVF4GP8lAYqZLaxInbdGICVAqonuBDA8wqUo+Ac\n"
#     b"SwIDAQAB\n"
#     b"-----END PUBLIC KEY-----"
# )

with open("public.pem", "rb") as f:
    public_key = f.read()

@user_router.get(
    "/{username}",
    response_model=UserResponse,
    # responses={"400": {"model": HTTPError}},
    description="activitypub user endpoint",
)
async def user(
    username: str,
    request: Request,
    # response: Response,
    ):
    if username != "nonbanana":
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # response.media_type = "application/activity+json"
    print(request.url.port)
    response_data = {
        "@context":  [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1"
	    ],
        "id": f"https://{config.HOST_NAME}/users/nonbanana",
        "inbox": f"https://{config.HOST_NAME}/inbox",
        "outbox": f"https://{config.HOST_NAME}/outbox",
        "type": "Person",
        "name": "nonbanana",
        "preferredUsername": "nonbanana",
        "publicKey": {
            "id": f"https://{config.HOST_NAME}/users/nonbanana#main-key",
            "owner": f"https://{config.HOST_NAME}/users/nonbanana",
            "publicKeyPem": public_key
        }
    }
    # response = Response(UserResponse(**response_data), status_code=status.HTTP_200_OK, media_type="application/activity+json")

    # Servers may discard the result if you do not set the appropriate content type
    # del response.headers['Content-Type']
    response = ActivityPubResponse(content=UserResponse(**response_data).json(by_alias=True), media_type="application/activity+json")
    # response = ActivityPubResponse(content=json.dumps(response_data), media_type="application/activity+json")
    response.headers['Content-Type'] = 'application/activity+json'
    # response
    # response.
    return response


@user_router.get(
    "/inbox",
    response_model=UserResponse,
    # responses={"400": {"model": HTTPError}},
    description="activitypub user endpoint",
)
async def user(
    username: str,
    # response: Response,
    request: Request,
    ):
    # if username != "nonbanana":
    #     HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # response.media_type = "application/activity+json"

    print(request.headers)
    print(request.data)
    
    return Response("", status=202)

