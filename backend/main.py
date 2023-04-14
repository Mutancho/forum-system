from fastapi import FastAPI

from routers.users import user_router

app = FastAPI()
app.include_router(user_router)

