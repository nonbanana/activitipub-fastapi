from fastapi import APIRouter
# import response

from activitypub.user import user_router
from activitypub.webfinger import webfinger_router

act_pub_router = APIRouter()

act_pub_router.include_router(user_router, prefix="/users", tags=["User"])
act_pub_router.include_router(webfinger_router,prefix="", tags=["Webfinger"])
# router.include_router(auth_router, prefix="/auth", tags=["Auth"])
__all__ = ["act_pub_router"]
