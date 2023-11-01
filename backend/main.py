from fastapi import FastAPI
from routers.users import router_user
from routers.categories import router_category
from routers.messages import router_message
from routers.topics import router_topic, router_all_topics
from routers.replies import router_reply
from database.connection import init_db, get_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    pool = await get_connection()
    await pool.close()


origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_user)
app.include_router(router_category)
app.include_router(router_message)
app.include_router(router_topic)
app.include_router(router_reply)
app.include_router(router_all_topics)
