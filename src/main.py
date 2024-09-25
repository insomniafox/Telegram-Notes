import structlog
from fastapi import FastAPI, APIRouter

from api.notes import router as notes_router
from api.users import router as users_router

app = FastAPI()


api_router = APIRouter(prefix="/api")

api_router.include_router(notes_router)
api_router.include_router(users_router)

app.include_router(api_router)
