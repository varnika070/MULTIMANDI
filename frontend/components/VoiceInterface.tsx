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
        <div className="flex flex-col items-center space-y-4 p-6 bg-white rounded-lg shadow-md">
            {/* Voice Recording Button */}
            <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`voice-button ${isRecording ? 'recording' : 'idle'}`}
                disabled={isPlaying}
            >
                {isRecording ? (
                    <MicOff className="w-8 h-8 text-white" />
                ) : (
                    <Mic className="w-8 h-8 text-white" />
                )}
            </button>

            <p className="text-sm text-gray-600 text-center">
                {isRecording ? 'Listening... Tap to stop' : 'Tap to start speaking'}
            </p>

            {/* Transcript Display */}
            {transcript && (
                <div className="w-full max-w-md">
                    <div className="bg-gray-50 p-3 rounded-lg border">
                        <p className="text-sm text-gray-700">{transcript}</p>
                    </div>

                    {/* Text-to-Speech Controls */}
                    <div className="flex justify-center mt-2">
                        <button
                            onClick={() => isPlaying ? stopSpeaking() : speakText(transcript)}
                            className="flex items-center space-x-2 px-3 py-1 bg-secondary-500 text-white rounded-md hover:bg-secondary-600 transition-colors"
                            disabled={!transcript}
                        >
                            {isPlaying ? (
                                <>
                                    <VolumeX className="w-4 h-4" />
                                    <span className="text-sm">Stop</span>
                                </>
                            ) : (
                                <>
                                    <Volume2 className="w-4 h-4" />
                                    <span className="text-sm">Play</span>
                                </>
                            )}
                        </button>
                    </div>
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className="w-full max-w-md">
                    <div className="bg-red-50 border border-red-200 p-3 rounded-lg">
                        <p className="text-sm text-red-700">{error}</p>
                    </div>
                </div>
            )}

            {/* Language Indicator */}
            <div className="text-xs text-gray-500">
                Language: {language}
            </div>
        </div>
    )
}