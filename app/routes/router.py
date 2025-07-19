from fastapi import APIRouter
from app.routes import auth_routes,local_routes,user_routes

api_router = APIRouter()

# Register routes with tags and prefixes
api_router.include_router(router=auth_routes.router, tags=["Authentication"], prefix="")
api_router.include_router(router=user_routes.router, tags=["Adminstration"], prefix="")
api_router.include_router(router=local_routes.router,tags=["Public_User"],prefix="")
