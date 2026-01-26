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
                return 'btn-secondary'
            case 'outline':
                return 'btn-outline'
            default:
                return 'btn-primary'
        }
    }

    const getSizeClasses = () => {
        switch (size) {
            case 'large':
                return 'py-6 px-8 text-touch-lg min-h-20 min-w-32'
            default:
                return 'py-4 px-6 text-touch-base min-h-16 min-w-24'
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
        ${className}
      `}
            aria-label={audioLabel || label}
        >
            {Icon && <Icon className="w-6 h-6" />}
            <span className="font-semibold">{label}</span>
            {children}
        </button>
    )
}