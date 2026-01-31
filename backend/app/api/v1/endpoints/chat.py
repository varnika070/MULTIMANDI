"""
Real-time chat endpoints with WebSocket support
"""

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.core.database import get_db
from app.services.chat import chat_manager
from app.services.speech import speech_service

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    
    try:
        # Wait for session join message
        data = await websocket.receive_text()
        message = json.loads(data)
        
        if message.get("type") == "join_session":
            session_id = message.get("session_id")
            if session_id:
                # Join existing session
                session = await chat_manager.join_session(session_id, user_id, websocket)
            else:
                # Create new session
                product_type = message.get("product_type")
                session = await chat_manager.create_session(user_id, product_type)
                await session.add_participant(user_id, websocket)
            
            if not session:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Failed to join session"
                }))
                return
            
            # Send session info
            await websocket.send_text(json.dumps({
                "type": "session_joined",
                "session_id": session.session_id,
                "product_type": session.product_type
            }))
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "chat_message":
                content = message.get("content", "")
                message_type = message.get("message_type", "text")
                audio_url = message.get("audio_url")
                
                # Send message to session
                await chat_manager.send_message(user_id, content, message_type, audio_url)
            
            elif message.get("type") == "voice_message":
                # Handle voice message processing
                transcription = message.get("transcription", "")
                audio_url = message.get("audio_url")
                
                # Process with AI if needed
                ai_response = await process_ai_response(transcription, user_id)
                
                # Send user message
                await chat_manager.send_message(user_id, transcription, "voice", audio_url)
                
                # Send AI response if available
                if ai_response:
                    await chat_manager.send_message("ai_assistant", ai_response, "ai")
    
    except WebSocketDisconnect:
        await chat_manager.leave_session(user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await chat_manager.leave_session(user_id)


@router.post("/sessions")
async def create_chat_session(
    user_id: str = Form(...),
    product_type: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat session"""
    session = await chat_manager.create_session(user_id, product_type)
    
    return {
        "session_id": session.session_id,
        "product_type": session.product_type,
        "created_at": session.created_at.isoformat()
    }


@router.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get message history for a session"""
    history = await chat_manager.get_session_history(session_id)
    return {
        "session_id": session_id,
        "messages": history,
        "total": len(history)
    }


@router.get("/sessions/active")
async def get_active_sessions():
    """Get list of active chat sessions"""
    sessions = chat_manager.get_active_sessions()
    return {
        "sessions": sessions,
        "total": len(sessions)
    }


@router.post("/sessions/{session_id}/voice")
async def process_voice_message(
    session_id: str,
    user_id: str = Form(...),
    audio: UploadFile = File(...),
    language: str = Form("en")
):
    """Process voice message in a chat session"""
    # Transcribe audio
    transcription_result = await speech_service.transcribe_audio(audio, language)
    
    if not transcription_result.get("transcription"):
        raise HTTPException(status_code=400, detail="Failed to transcribe audio")
    
    transcription = transcription_result["transcription"]
    
    # Send message to session
    message = await chat_manager.send_message(user_id, transcription, "voice")
    
    # Generate AI response
    ai_response = await process_ai_response(transcription, user_id)
    if ai_response:
        ai_message = await chat_manager.send_message("ai_assistant", ai_response, "ai")
        
        return {
            "user_message": message.to_dict() if message else None,
            "ai_response": ai_message.to_dict() if ai_message else None,
            "transcription": transcription_result
        }
    
    return {
        "user_message": message.to_dict() if message else None,
        "transcription": transcription_result
    }


async def process_ai_response(user_message: str, user_id: str) -> Optional[str]:
    """Process user message and generate AI response"""
    message_lower = user_message.lower()
    
    # Price inquiry responses
    if any(word in message_lower for word in ['price', 'cost', 'rate', 'kimat']):
        products = ['rice', 'wheat', 'onion', 'potato', 'tomato', 'cotton']
        mentioned_product = None
        
        for product in products:
            if product in message_lower:
                mentioned_product = product
                break
        
        if mentioned_product:
            return f"The current market price for {mentioned_product} is around ₹2,500 per quintal. Would you like detailed price analysis or want to discuss trading?"
        else:
            return "I can help you with current market prices. Which product are you interested in? I have data for rice, wheat, onion, potato, tomato, and cotton."
    
    # Trading responses
    elif any(word in message_lower for word in ['sell', 'buy', 'trade']):
        return "Great! I can help you with trading. Let me know what product and quantity you're interested in, and I'll provide current market rates and connect you with potential buyers or sellers."
    
    # Greeting responses
    elif any(word in message_lower for word in ['hello', 'hi', 'namaste', 'namaskar']):
        return "Hello! Welcome to OpenMandi. I'm your AI trading assistant. I can help you with current market prices, trading advice, and connecting with other traders. What would you like to know?"
    
    # Default response
    else:
        return "I understand you're interested in agricultural trading. I can help with current prices, market trends, and trading advice. Try asking about specific products or say 'hello' to get started."