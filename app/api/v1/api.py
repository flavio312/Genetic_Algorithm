from fastapi import APIRouter
from app.api.v1.endpoints import genetic_algorithm

api_router = APIRouter()

api_router.include_router(
    genetic_algorithm.router, 
    prefix="/algoritmo-genetico", 
    tags=["Algoritmo Genético"]
)

