from fastapi import FastAPI
from src.routes import users, cache
import redis.asyncio as redis
from src.conf.config import settings

app = FastAPI()

@app.on_event("startup")
async def startup():
    """Initializes Redis connection."""
    app.state.redis = await redis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )

@app.on_event("shutdown")
async def shutdown():
    """Closes Redis connection."""
    await app.state.redis.close()


app.include_router(users.router, prefix="/api")
app.include_router(cache.router, prefix="/api")
app.include_router(cache.cat_router)
