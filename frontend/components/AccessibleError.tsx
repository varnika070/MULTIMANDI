'use client'

import React, { useState, useEffect } from 'react'
import { AlertTriangle, Info, X, Volume2, RefreshCw } from 'lucide-react'

interface ErrorMessage {
    simple: string
    detailed: string
    audio: string
}

interface Visual {
    color: string
    icon: string
    animation: string
    duration: number
}

interface Recovery {
    steps: string[]
    audio_steps: string[]
    prevention_tips: string[]
}

interface AccessibleErrorProps {
    error_id: string
    category: string
    severity: 'info' | 'warning' | 'error' | 'critical'
    title: string
    message: ErrorMessage
    visual: Visual
    recovery: Recovery
    multilingual: Record<string, string>
    accessibility: Record<string, boolean>
    onDismiss?: () => void
    onRetry?: () => void
    language?: string
}

const AccessibleError: React.FC<AccessibleErrorProps> = ({
    error_id,
    category,
    severity,
    title,
    message,
    visual,
    recovery,
    multilingual,
    accessibility,
    onDismiss,
    onRetry,
    language = 'english'
}) => {
    const [isExpanded, setIsExpanded] = useState(false)
    const [hasPlayedAudio, setHasPlayedAudio] = useState(false)
    const [currentStep, setCurrentStep] = useState(0)

    // Auto-dismiss for info messages
    useEffect(() => {
        if (severity === 'info' && visual.duration > 0) {
            const timer = setTimeout(() => {
                onDismiss?.()
            }, visual.duration)
            return () => clearTimeout(timer)
        }
    }, [severity, visual.duration, onDismiss])

    // Play audio message if accessibility is enabled
    useEffect(() => {
        if (accessibility.audio_feedback && !hasPlayedAudio) {
            playAudioMessage()
            setHasPlayedAudio(true)
        }
    }, [accessibility.audio_feedback, hasPlayedAudio])

    const playAudioMessage = () => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(message.audio)
            utterance.rate = 0.8
            utterance.volume = 0.8

            // Set language if available
            if (language !== 'english') {
                const langMap: Record<string, string> = {
                    'hindi': 'hi-IN',
                    'telugu': 'te-IN',
                    'tamil': 'ta-IN',
                    'kannada': 'kn-IN'
                }
                utterance.lang = langMap[language] || 'en-US'
            }

            speechSynthesis.speak(utterance)
        }
    }

    const playRecoveryStep = (step: string) => {
        if ('speechSynthesis' in window && accessibility.voice_guidance) {
            const utterance = new SpeechSynthesisUtterance(step)
            utterance.rate = 0.8
            speechSynthesis.speak(utterance)
        }
    }

    const getIcon = () => {
        switch (severity) {
            case 'info':
                return <Info className="w-6 h-6" />
            case 'warning':
                return <AlertTriangle className="w-6 h-6" />
            case 'error':
            case 'critical':
                return <AlertTriangle className="w-6 h-6" />
            default:
                return <Info className="w-6 h-6" />
        }
    }

    const getSeverityClasses = () => {
        const baseClasses = "rounded-lg border-l-4 p-4 shadow-lg"

        switch (severity) {
            case 'info':
                return `${baseClasses} bg-blue-50 border-blue-400 text-blue-800`
            case 'warning':
                return `${baseClasses} bg-yellow-50 border-yellow-400 text-yellow-800`
            case 'error':
                return `${baseClasses} bg-red-50 border-red-400 text-red-800`
            case 'critical':
                return `${baseClasses} bg-red-100 border-red-600 text-red-900 animate-pulse`
            default:
                return `${baseClasses} bg-gray-50 border-gray-400 text-gray-800`
        }
    }

    const getDisplayMessage = () => {
        // Use multilingual message if available
        if (language !== 'english' && multilingual[language]) {
            return multilingual[language]
        }

        // Use simple or detailed message based on accessibility settings
        return accessibility.simple_language ? message.simple : message.detailed
    }

    return (
        <div
            className={`${getSeverityClasses()} ${visual.animation === 'shake' ? 'animate-bounce' : ''}`}
            role="alert"
            aria-live={severity === 'critical' ? 'assertive' : 'polite'}
            style={{
                fontSize: accessibility.large_text ? '1.125rem' : '1rem',
                lineHeight: accessibility.large_text ? '1.75' : '1.5'
            }}
        >
            <div className="flex items-start">
                <div className="flex-shrink-0" style={{ color: visual.color }}>
                    {getIcon()}
                </div>

                <div className="ml-3 flex-1">
                    <h3 className={`font-medium ${accessibility.large_text ? 'text-lg' : 'text-base'}`}>
                        {title}
                    </h3>

                    <div className="mt-2">
                        <p className={`${accessibility.large_text ? 'text-base' : 'text-sm'}`}>
                            {getDisplayMessage()}
                        </p>
                    </div>

                    {/* Recovery Steps */}
                    {recovery.steps.length > 0 && (
                        <div className="mt-4">
                            <button
                                onClick={() => setIsExpanded(!isExpanded)}
                                className="text-sm font-medium underline hover:no-underline focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                                aria-expanded={isExpanded}
                            >
                                {isExpanded ? 'Hide' : 'Show'} recovery steps
                            </button>

                            {isExpanded && (
                                <div className="mt-3 space-y-2">
                                    <h4 className="font-medium text-sm">How to fix this:</h4>
                                    <ol className="list-decimal list-inside space-y-1 text-sm">
                                        {recovery.steps.map((step, index) => (
                                            <li
                                                key={index}
                                                className="flex items-center justify-between"
                                            >
                                                <span className="flex-1">{step}</span>
                                                {accessibility.voice_guidance && (
                                                    <button
                                                        onClick={() => playRecoveryStep(step)}
                                                        className="ml-2 p-1 text-gray-500 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
                                                        aria-label={`Play audio for step ${index + 1}`}
                                                    >
                                                        <Volume2 className="w-4 h-4" />
                                                    </button>
                                                )}
                                            </li>
                                        ))}
                                    </ol>

                                    {/* Prevention Tips */}
                                    {recovery.prevention_tips.length > 0 && (
                                        <div className="mt-3 p-3 bg-gray-50 rounded">
                                            <h5 className="font-medium text-sm mb-2">Prevention tips:</h5>
                                            <ul className="list-disc list-inside space-y-1 text-xs">
                                                {recovery.prevention_tips.map((tip, index) => (
                                                    <li key={index}>{tip}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    )}

                    {/* Action Buttons */}
                    <div className="mt-4 flex flex-wrap gap-2">
                        {onRetry && (
                            <button
                                onClick={onRetry}
                                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                            >
                                <RefreshCw className="w-4 h-4 mr-1" />
                                Try Again
                            </button>
                        )}

                        {accessibility.audio_feedback && (
                            <button
                                onClick={playAudioMessage}
                                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                            >
                                <Volume2 className="w-4 h-4 mr-1" />
                                Repeat Audio
                            </button>
                        )}
                    </div>
                </div>

                {/* Dismiss Button */}
                {onDismiss && (
                    <div className="ml-auto pl-3">
                        <button
                            onClick={onDismiss}
                            className="inline-flex text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-md p-1"
                            aria-label="Dismiss error"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

export default AccessibleError