from fastapi import FastAPI
from backend.routers.users import router_user
from backend.routers.categories import router_category
from backend.routers.messages import router_message
from backend.routers.topics import router_topic, router_all_topics
from backend.routers.replies import router_reply
from backend.database.connection import init_db, get_connection
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
    "http://localhost:4200",  # This is the origin for your request
    # You can add other origins if needed
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
