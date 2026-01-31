'use client'

import { useState, useCallback } from 'react'

interface ErrorData {
    error_id: string
    category: string
    severity: 'info' | 'warning' | 'error' | 'critical'
    title: string
    message: {
        simple: string
        detailed: string
        audio: string
    }
    visual: {
        color: string
        icon: string
        animation: string
        duration: number
    }
    recovery: {
        steps: string[]
        audio_steps: string[]
        prevention_tips: string[]
    }
    multilingual: Record<string, string>
    accessibility: Record<string, boolean>
    timestamp: string
}

interface UseAccessibleErrorsReturn {
    errors: ErrorData[]
    showError: (error: ErrorData) => void
    dismissError: (errorId: string) => void
    clearAllErrors: () => void
    createNetworkError: (type?: string, context?: any) => Promise<void>
    createValidationError: (type: string, context?: any) => Promise<void>
    createSpeechError: (type: string, context?: any) => Promise<void>
    createPriceError: (type: string, context?: any) => Promise<void>
    createNegotiationWarning: (type: string, context?: any) => Promise<void>
}

export const useAccessibleErrors = (): UseAccessibleErrorsReturn => {
    const [errors, setErrors] = useState<ErrorData[]>([])

    const showError = useCallback((error: ErrorData) => {
        setErrors(prev => {
            // Remove any existing error with the same ID
            const filtered = prev.filter(e => e.error_id !== error.error_id)
            return [...filtered, error]
        })
    }, [])

    const dismissError = useCallback((errorId: string) => {
        setErrors(prev => prev.filter(e => e.error_id !== errorId))
    }, [])

    const clearAllErrors = useCallback(() => {
        setErrors([])
    }, [])

    const createNetworkError = useCallback(async (type: string = 'connection_failed', context?: any) => {
        try {
            const response = await fetch('/api/v1/errors/network', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    error_type: type,
                    context: context || {}
                })
            })

            if (response.ok) {
                const errorData = await response.json()
                showError(errorData)
            } else {
                // Fallback error
                showError(createFallbackError('Network Error', 'Connection problem occurred'))
            }
        } catch (error) {
            showError(createFallbackError('Network Error', 'Unable to connect to server'))
        }
    }, [showError])

    const createValidationError = useCallback(async (type: string, context?: any) => {
        try {
            const response = await fetch('/api/v1/errors/validation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    error_type: type,
                    context: context || {}
                })
            })

            if (response.ok) {
                const errorData = await response.json()
                showError(errorData)
            } else {
                showError(createFallbackError('Validation Error', 'Please check your input'))
            }
        } catch (error) {
            showError(createFallbackError('Validation Error', 'Input validation failed'))
        }
    }, [showError])

    const createSpeechError = useCallback(async (type: string, context?: any) => {
        try {
            const response = await fetch('/api/v1/errors/speech', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    error_type: type,
                    context: context || {}
                })
            })

            if (response.ok) {
                const errorData = await response.json()
                showError(errorData)
            } else {
                showError(createFallbackError('Speech Error', 'Voice processing failed'))
            }
        } catch (error) {
            showError(createFallbackError('Speech Error', 'Cannot process voice input'))
        }
    }, [showError])

    const createPriceError = useCallback(async (type: string, context?: any) => {
        try {
            const response = await fetch('/api/v1/errors/price', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    error_type: type,
                    context: context || {}
                })
            })

            if (response.ok) {
                const errorData = await response.json()
                showError(errorData)
            } else {
                showError(createFallbackError('Price Error', 'Price data unavailable'))
            }
        } catch (error) {
            showError(createFallbackError('Price Error', 'Cannot get current prices'))
        }
    }, [showError])

    const createNegotiationWarning = useCallback(async (type: string, context?: any) => {
        try {
            const response = await fetch('/api/v1/errors/negotiation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    error_type: type,
                    context: context || {}
                })
            })

            if (response.ok) {
                const errorData = await response.json()
                showError(errorData)
            } else {
                showError(createFallbackError('Trading Warning', 'Please review this transaction carefully'))
            }
        } catch (error) {
            showError(createFallbackError('Trading Warning', 'Potential trading risk detected'))
        }
    }, [showError])

    const createFallbackError = (title: string, message: string): ErrorData => {
        return {
            error_id: `fallback_${Date.now()}`,
            category: 'system',
            severity: 'error',
            title,
            message: {
                simple: message,
                detailed: message,
                audio: message
            },
            visual: {
                color: '#EF4444',
                icon: 'error',
                animation: 'fade-in',
                duration: 5000
            },
            recovery: {
                steps: ['Try refreshing the page', 'Check your internet connection', 'Contact support if problem persists'],
                audio_steps: ['Try refreshing the page', 'Check your internet connection'],
                prevention_tips: ['Ensure stable internet connection', 'Keep the app updated']
            },
            multilingual: {},
            accessibility: {
                high_contrast: true,
                large_text: false,
                audio_feedback: true,
                simple_language: true
            },
            timestamp: new Date().toISOString()
        }
    }

    return {
        errors,
        showError,
        dismissError,
        clearAllErrors,
        createNetworkError,
        createValidationError,
        createSpeechError,
        createPriceError,
        createNegotiationWarning
    }
}

export default useAccessibleErrors