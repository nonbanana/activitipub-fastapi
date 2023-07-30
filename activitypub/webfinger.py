from typing import List
import json
from fastapi import APIRouter, Depends, Query, HTTPException, status, Response
from core.config import config

# class ActivityPubResponse(Response):
#     media_type = "application/activity+json"

webfinger_router = APIRouter()

@webfinger_router.get(
    "/.well-known/webfinger",
    # responses={"400": {"model": HTTPError}},
    description="activitypub user endpoint",
)
def webfinger(resource: str = Query(..., alias="resource")):
    # resource = request.args.get('resource')
    print('asdf')
    if resource != f"acct:nonbanana@{config.HOST_NAME}":
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    response = Response(
        content=json.dumps({
            "subject": f"acct:nonbanana@{config.HOST_NAME}",
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": f"https://{config.HOST_NAME}/users/nonbanana"
                }
            ]
        })
    )
    

    # Servers may discard the result if you do not set the appropriate content type
    response.headers['Content-Type'] = 'application/jrd+json'
    
    return response