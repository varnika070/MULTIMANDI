"""
Real-time chat service with WebSocket support
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.database import AsyncSessionLocal


class ChatMessage:
    def __init__(
        self, 
        message_id: str,
        session_id: str,
        sender_id: str,
        content: str,
        message_type: str = "text",
        audio_url: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        self.message_id = message_id
        self.session_id = session_id
        self.sender_id = sender_id
        self.content = content
        self.message_type = message_type
        self.audio_url = audio_url
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "session_id": self.session_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "message_type": self.message_type,
            "audio_url": self.audio_url,
            "timestamp": self.timestamp.isoformat()
        }


class ChatSession:
    def __init__(self, session_id: str, product_type: Optional[str] = None):
        self.session_id = session_id
        self.product_type = product_type
        self.participants: Set[str] = set()
        self.connections: Dict[str, WebSocket] = {}
        self.messages: List[ChatMessage] = []
        self.created_at = datetime.utcnow()
        self.is_active = True
    
    async def add_participant(self, user_id: str, websocket: WebSocket):
        """Add a participant to the chat session"""
        self.participants.add(user_id)
        self.connections[user_id] = websocket
        
        # Send welcome message
        welcome_msg = ChatMessage(
            message_id=str(uuid.uuid4()),
            session_id=self.session_id,
            sender_id="system",
            content=f"Welcome to OpenMandi chat! You can discuss {self.product_type or 'agricultural products'} here.",
            message_type="system"
        )
        
        await self.broadcast_message(welcome_msg)
    
    async def remove_participant(self, user_id: str):
        """Remove a participant from the chat session"""
        self.participants.discard(user_id)
        if user_id in self.connections:
            del self.connections[user_id]
        
        if not self.participants:
            self.is_active = False
    
    async def broadcast_message(self, message: ChatMessage):
        """Broadcast message to all participants"""
        self.messages.append(message)
        message_data = json.dumps(message.to_dict())
        
        # Send to all connected participants
        disconnected_users = []
        for user_id, websocket in self.connections.items():
            try:
                await websocket.send_text(message_data)
            except Exception:
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            await self.remove_participant(user_id)
    
    async def add_message(self, sender_id: str, content: str, message_type: str = "text", audio_url: Optional[str] = None):
        """Add a new message to the session"""
        message = ChatMessage(
            message_id=str(uuid.uuid4()),
            session_id=self.session_id,
            sender_id=sender_id,
            content=content,
            message_type=message_type,
            audio_url=audio_url
        )
        
        await self.broadcast_message(message)
        return message


class ChatManager:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id
    
    async def create_session(self, user_id: str, product_type: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id, product_type)
        self.sessions[session_id] = session
        self.user_sessions[user_id] = session_id
        return session
    
    async def join_session(self, session_id: str, user_id: str, websocket: WebSocket) -> Optional[ChatSession]:
        """Join an existing chat session"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        if not session.is_active:
            return None
        
        await session.add_participant(user_id, websocket)
        self.user_sessions[user_id] = session_id
        return session
    
    async def leave_session(self, user_id: str):
        """Leave current chat session"""
        if user_id not in self.user_sessions:
            return
        
        session_id = self.user_sessions[user_id]
        if session_id in self.sessions:
            session = self.sessions[session_id]
            await session.remove_participant(user_id)
            
            # Clean up empty sessions
            if not session.is_active:
                del self.sessions[session_id]
        
        del self.user_sessions[user_id]
    
    async def get_user_session(self, user_id: str) -> Optional[ChatSession]:
        """Get current session for a user"""
        if user_id not in self.user_sessions:
            return None
        
        session_id = self.user_sessions[user_id]
        return self.sessions.get(session_id)
    
    async def send_message(self, user_id: str, content: str, message_type: str = "text", audio_url: Optional[str] = None):
        """Send a message in user's current session"""
        session = await self.get_user_session(user_id)
        if not session:
            return None
        
        return await session.add_message(user_id, content, message_type, audio_url)
    
    async def get_session_history(self, session_id: str) -> List[Dict]:
        """Get message history for a session"""
        if session_id not in self.sessions:
            return []
        
        session = self.sessions[session_id]
        return [msg.to_dict() for msg in session.messages]
    
    def get_active_sessions(self) -> List[Dict]:
        """Get list of active sessions"""
        return [
            {
                "session_id": session.session_id,
                "product_type": session.product_type,
                "participants": len(session.participants),
                "created_at": session.created_at.isoformat(),
                "message_count": len(session.messages)
            }
            for session in self.sessions.values()
            if session.is_active
        ]


# Global chat manager instance
chat_manager = ChatManager()