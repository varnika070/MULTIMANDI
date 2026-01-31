"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import users, price, chat, speech, negotiation, ethical_safeguards, errors

api_router = APIRouter()

# Health check endpoint
@api_router.get("/health")
async def health():
    """API health check"""
    return {"status": "healthy", "version": "1.0.0"}

# Include endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(price.router, prefix="/price", tags=["price"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(speech.router, prefix="/speech", tags=["speech"])
api_router.include_router(negotiation.router, prefix="/negotiation", tags=["negotiation"])
api_router.include_router(ethical_safeguards.router, prefix="/ethics", tags=["ethical-safeguards"])
api_router.include_router(errors.router, prefix="/errors", tags=["accessible-errors"])