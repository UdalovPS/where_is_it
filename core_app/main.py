import logging

from fastapi import FastAPI

from routers.spots import router as spots_router

# настраиваем логирование
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s")


app = FastAPI(title='Where is it APP')

app.include_router(spots_router, prefix="/api")


