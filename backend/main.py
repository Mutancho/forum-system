from fastapi import FastAPI
from routers.users import router_user
from routers.categories import router_category
from routers.messages import router_message
from routers.topics import router_topic, router_all_topics
from routers.replies import router_reply

app = FastAPI()
app.include_router(router_user)
app.include_router(router_category)
app.include_router(router_message)
app.include_router(router_topic)
app.include_router(router_reply)
app.include_router(router_all_topics)
