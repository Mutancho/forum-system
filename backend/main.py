from fastapi import FastAPI
from routers.users import router_user
from routers.categories import router_category
from routers.messages import router_message

app = FastAPI()
app.include_router(router_user)
app.include_router(router_category)
app.include_router(router_message)
