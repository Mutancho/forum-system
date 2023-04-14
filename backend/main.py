from fastapi import FastAPI
from routers.users import user_router
from backend.routers.categories import router_category

app = FastAPI()
app.include_router(user_router)
app.include_router(router_category)
