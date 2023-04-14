from fastapi import FastAPI
from backend.routers.categories import router_category

app = FastAPI()
app.include_router(router_category)
