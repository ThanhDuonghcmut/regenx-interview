from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from constant import API_PREFIX
from routes import router

app = FastAPI(
    title="Demo for interview",
    openapi_url=f"{API_PREFIX}/openapi.json"
)

# Set all CORS enabled origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)