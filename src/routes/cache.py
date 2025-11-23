import json
import httpx
from fastapi import APIRouter, HTTPException, Depends, Request
import redis.asyncio as redis

router = APIRouter(prefix="/cache", tags=["cache"])
cat_router = APIRouter(tags=["cat_api"])

CAT_API_URL = "https://catfact.ninja/fact"
CACHE_KEY = "cat_fact"

# Видаляємо глобальну ініціалізацію клієнта, яка викликала помилку
# redis_client = redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)


# Функція-залежність для отримання клієнта Redis
async def get_redis_client(request: Request) -> redis.Redis:
    return request.app.state.redis


@router.post("/set")
async def set_cache(key: str, value: str, redis_client: redis.Redis = Depends(get_redis_client)):
    await redis_client.set(key, value)
    return {"status": "ok", "key": key, "value": value}

@router.get("/get/{key}")
async def get_cache(key: str, redis_client: redis.Redis = Depends(get_redis_client)):
    value = await redis_client.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}

@cat_router.get("/cat-fact", summary="Get a random cat fact")
async def get_cat_fact_from_api(
    redis_client: redis.Redis = Depends(get_redis_client)
):
    try:
        cached_fact = await redis_client.get(CACHE_KEY)
        if cached_fact:
            return json.loads(cached_fact)

        async with httpx.AsyncClient() as client:
            response = await client.get(CAT_API_URL)
            response.raise_for_status()
            data = response.json()

        await redis_client.set(CACHE_KEY, json.dumps(data), ex=60)
        return data
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching from catfact.ninja: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
