'use client'

import { ReactNode } from 'react'
import { LucideIcon } from 'lucide-react'

interface BigButtonProps {
    icon?: LucideIcon
    label: string
    audioLabel?: string
    onClick: () => void
    variant?: 'primary' | 'secondary' | 'outline'
    size?: 'normal' | 'large'
    disabled?: boolean
    className?: string
    children?: ReactNode
}

export default function BigButton({
    icon: Icon,
    label,
    audioLabel,
    onClick,
    variant = 'primary',
    size = 'normal',
    disabled = false,
    className = '',
    children
}: BigButtonProps) {

    const handleClick = () => {
        // Speak the audio label if provided and speech synthesis is available
        if (audioLabel && 'speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(audioLabel)
            utterance.rate = 0.9
            speechSynthesis.speak(utterance)
        }

        onClick()
    }

    const getVariantClasses = () => {
        switch (variant) {
            case 'secondary':
                return 'bg-gradient-to-r from-secondary-500 to-secondary-600 hover:from-secondary-600 hover:to-secondary-700 text-white shadow-lg hover:shadow-xl'
            case 'outline':
                return 'border-2 border-primary-500 text-primary-600 hover:bg-gradient-to-r hover:from-primary-500 hover:to-primary-600 hover:text-white bg-white/90 backdrop-blur-sm shadow-lg hover:shadow-xl hover:border-transparent'
            default:
                return 'bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white shadow-lg hover:shadow-xl'
        }
    }

    const getSizeClasses = () => {
        switch (size) {
            case 'large':
                return 'py-6 px-8 text-touch-lg min-h-20 min-w-32 rounded-2xl'
            default:
                return 'py-4 px-6 text-touch-base min-h-16 min-w-24 rounded-xl'
        }
    }

    return (
        <button
            onClick={handleClick}
            disabled={disabled}
            className={`
        ${getVariantClasses()}
        ${getSizeClasses()}
        flex items-center justify-center space-x-3
        disabled:opacity-50 disabled:cursor-not-allowed
        focus:ring-4 focus:ring-primary-200
        transition-all duration-200 transform hover:scale-105 active:scale-95
        font-semibold
        ${className}
      `}
            aria-label={audioLabel || label}
        >
            {Icon && <Icon className="w-6 h-6" />}
            <span>{label}</span>
            {children}
        </button>
    )
}