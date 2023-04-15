from fastapi import FastAPI
from routers.users import user_router
from routers.categories import router_category
from routers.messages import message_router

app = FastAPI()
app.include_router(user_router)
app.include_router(router_category)
app.include_router(message_router)
