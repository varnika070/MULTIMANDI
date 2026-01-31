"""
Speech processing endpoints
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.services.speech import speech_service

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = Form("en"),
    dialect_hints: Optional[str] = Form(None)
):
    """Transcribe audio to text"""
    if not audio.content_type or not audio.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Invalid audio file")
    
    dialect_list = dialect_hints.split(',') if dialect_hints else None
    
    result = await speech_service.transcribe_audio(
        audio_file=audio,
        language=language,
        dialect_hints=dialect_list
    )
    
    return result


@router.post("/synthesize")
async def synthesize_speech(
    text: str = Form(...),
    language: str = Form("en"),
    voice_profile: Optional[str] = Form(None)
):
    """Convert text to speech"""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = await speech_service.synthesize_speech(
        text=text,
        language=language,
        voice_profile=voice_profile
    )
    
    return result


@router.post("/detect-language")
async def detect_language(audio: UploadFile = File(...)):
    """Detect language from audio"""
    if not audio.content_type or not audio.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Invalid audio file")
    
    result = await speech_service.detect_language(audio)
    return result


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": speech_service.get_supported_languages(),
        "total": len(speech_service.get_supported_languages())
    }


@router.post("/translate-terms")
async def translate_agricultural_terms(
    text: str = Form(...),
    source_language: str = Form("en"),
    target_language: str = Form("hi")
):
    """Translate agricultural terminology between languages"""
    result = await speech_service.process_agricultural_terms(
        text=text,
        source_language=source_language,
        target_language=target_language
    )
    
    return result