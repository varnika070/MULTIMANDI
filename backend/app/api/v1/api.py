"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import users, price

api_router = APIRouter()

# Health check endpoint
@api_router.get("/health")
async def health():
    """API health check"""
    return {"status": "healthy", "version": "1.0.0"}

# Include endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(price.router, prefix="/price", tags=["price"])