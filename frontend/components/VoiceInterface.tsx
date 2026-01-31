'use client'

import { useState, useRef, useEffect } from 'react'
import { Mic, MicOff, Volume2, VolumeX } from 'lucide-react'

interface VoiceInterfaceProps {
    onTranscription?: (text: string) => void
    onAudioReceived?: (audioUrl: string) => void
    language?: string
}

export default function VoiceInterface({
    onTranscription,
    onAudioReceived,
    language = 'en-US'
}: VoiceInterfaceProps) {
    const [isRecording, setIsRecording] = useState(false)
    const [isPlaying, setIsPlaying] = useState(false)
    const [transcript, setTranscript] = useState('')
    const [error, setError] = useState('')

    const mediaRecorderRef = useRef<MediaRecorder | null>(null)
    const audioChunksRef = useRef<Blob[]>([])
    const recognitionRef = useRef<SpeechRecognition | null>(null)

    useEffect(() => {
        // Initialize speech recognition if available
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
            recognitionRef.current = new SpeechRecognition()

            if (recognitionRef.current) {
                recognitionRef.current.continuous = false
                recognitionRef.current.interimResults = true
                recognitionRef.current.lang = language

                recognitionRef.current.onresult = (event) => {
                    let finalTranscript = ''
                    let interimTranscript = ''

                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript
                        if (event.results[i].isFinal) {
                            finalTranscript += transcript
                        } else {
                            interimTranscript += transcript
                        }
                    }

                    const fullTranscript = finalTranscript || interimTranscript
                    setTranscript(fullTranscript)

                    if (finalTranscript && onTranscription) {
                        onTranscription(finalTranscript)
                    }
                }

                recognitionRef.current.onerror = (event) => {
                    setError(`Speech recognition error: ${event.error}`)
                    setIsRecording(false)
                }

                recognitionRef.current.onend = () => {
                    setIsRecording(false)
                }
            }
        }
    }, [language, onTranscription])

    const startRecording = async () => {
        try {
            setError('')
            setTranscript('')

            // Start speech recognition
            if (recognitionRef.current) {
                recognitionRef.current.start()
            }

            // Start audio recording
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            const mediaRecorder = new MediaRecorder(stream)
            mediaRecorderRef.current = mediaRecorder
            audioChunksRef.current = []

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data)
                }
            }

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
                const audioUrl = URL.createObjectURL(audioBlob)

                if (onAudioReceived) {
                    onAudioReceived(audioUrl)
                }

                // Stop all tracks
                stream.getTracks().forEach(track => track.stop())
            }

            mediaRecorder.start()
            setIsRecording(true)

        } catch (err) {
            setError('Failed to access microphone. Please check permissions.')
            console.error('Recording error:', err)
        }
    }

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop()
        }

        if (recognitionRef.current) {
            recognitionRef.current.stop()
        }

        setIsRecording(false)
    }

    const speakText = (text: string) => {
        if ('speechSynthesis' in window) {
            setIsPlaying(true)

            const utterance = new SpeechSynthesisUtterance(text)
            utterance.lang = language
            utterance.rate = 0.9
            utterance.pitch = 1

            utterance.onend = () => {
                setIsPlaying(false)
            }

            utterance.onerror = () => {
                setIsPlaying(false)
                setError('Text-to-speech failed')
            }

            speechSynthesis.speak(utterance)
        } else {
            setError('Text-to-speech not supported')
        }
    }

    const stopSpeaking = () => {
        if ('speechSynthesis' in window) {
            speechSynthesis.cancel()
            setIsPlaying(false)
        }
    }

    return (
        <div className="flex flex-col items-center space-y-6 p-8 bg-white/90 backdrop-blur-md rounded-2xl shadow-xl border border-white/20">
            {/* Voice Recording Button */}
            <div className="relative">
                <button
                    onClick={isRecording ? stopRecording : startRecording}
                    className={`voice-button ${isRecording ? 'recording' : 'idle'} relative overflow-hidden`}
                    disabled={isPlaying}
                >
                    <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"></div>
                    <div className="relative z-10">
                        {isRecording ? (
                            <MicOff className="w-8 h-8 text-white" />
                        ) : (
                            <Mic className="w-8 h-8 text-white" />
                        )}
                    </div>
                    {isRecording && (
                        <div className="absolute inset-0 bg-red-500/20 rounded-full animate-ping"></div>
                    )}
                </button>
            </div>

            <div className="text-center">
                <p className="text-sm font-medium text-gray-700 mb-1">
                    {isRecording ? 'Listening... Tap to stop' : 'Tap to start speaking'}
                </p>
                <p className="text-xs text-gray-500 mb-2">
                    Voice recognition powered by AI
                </p>
                <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg px-3 py-1 border border-yellow-200">
                    <p className="text-xs text-yellow-800 font-medium">
                        🤖 Prototype voice AI - Simulated speech processing
                    </p>
                </div>
            </div>

            {/* Transcript Display */}
            {transcript && (
                <div className="w-full max-w-md">
                    <div className="bg-gradient-to-r from-primary-50 to-secondary-50 p-4 rounded-xl border border-primary-100 shadow-sm">
                        <div className="flex items-start space-x-3">
                            <div className="w-6 h-6 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center flex-shrink-0 mt-0.5">
                                <Mic className="w-3 h-3 text-white" />
                            </div>
                            <p className="text-sm text-gray-700 leading-relaxed flex-1">{transcript}</p>
                        </div>
                    </div>

                    {/* Text-to-Speech Controls */}
                    <div className="flex justify-center mt-4">
                        <button
                            onClick={() => isPlaying ? stopSpeaking() : speakText(transcript)}
                            className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-secondary-500 to-secondary-600 text-white rounded-xl hover:from-secondary-600 hover:to-secondary-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
                            disabled={!transcript}
                        >
                            {isPlaying ? (
                                <>
                                    <VolumeX className="w-4 h-4" />
                                    <span className="text-sm font-medium">Stop</span>
                                </>
                            ) : (
                                <>
                                    <Volume2 className="w-4 h-4" />
                                    <span className="text-sm font-medium">Play</span>
                                </>
                            )}
                        </button>
                    </div>
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className="w-full max-w-md">
                    <div className="bg-red-50 border border-red-200 p-4 rounded-xl shadow-sm">
                        <div className="flex items-start space-x-3">
                            <div className="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center flex-shrink-0 mt-0.5">
                                <span className="text-white text-xs font-bold">!</span>
                            </div>
                            <p className="text-sm text-red-700 leading-relaxed flex-1">{error}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Language Indicator */}
            <div className="flex items-center justify-center space-x-2 text-xs bg-gradient-to-r from-gray-50 to-slate-50 px-4 py-2 rounded-full border border-gray-200">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                <span className="text-gray-600 font-medium">Active Language: {language}</span>
            </div>
        </div>
    )
}