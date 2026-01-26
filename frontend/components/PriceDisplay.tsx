'use client'

import { useState } from 'react'
import { TrendingUp, TrendingDown, Minus, Volume2 } from 'lucide-react'

interface PriceDisplayProps {
    product: string
    price: number
    unit: string
    trend: 'up' | 'down' | 'stable'
    confidence?: number
    explanation?: string
    factors?: string[]
}

export default function PriceDisplay({
    product,
    price,
    unit,
    trend,
    confidence = 0.85,
    explanation,
    factors = []
}: PriceDisplayProps) {
    const [showDetails, setShowDetails] = useState(false)

    const getTrendIcon = () => {
        switch (trend) {
            case 'up':
                return <TrendingUp className="w-5 h-5 text-green-600" />
            case 'down':
                return <TrendingDown className="w-5 h-5 text-red-600" />
            default:
                return <Minus className="w-5 h-5 text-gray-600" />
        }
    }

    const getTrendColor = () => {
        switch (trend) {
            case 'up':
                return 'text-green-600 bg-green-50 border-green-200'
            case 'down':
                return 'text-red-600 bg-red-50 border-red-200'
            default:
                return 'text-gray-600 bg-gray-50 border-gray-200'
        }
    }

    const speakPrice = () => {
        if ('speechSynthesis' in window) {
            const text = `${product} price is ${price} rupees per ${unit}. Market trend is ${trend}. Confidence level is ${Math.round(confidence * 100)} percent.`
            const utterance = new SpeechSynthesisUtterance(text)
            utterance.rate = 0.8
            speechSynthesis.speak(utterance)
        }
    }

    return (
        <div className="price-display">
            {/* Header */}
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-bold text-gray-900">{product}</h3>
                    <p className="text-sm text-gray-600">Current Market Price</p>
                </div>

                <div className="flex items-center space-x-2">
                    {/* Trend Indicator */}
                    <div className={`flex items-center space-x-1 px-2 py-1 rounded-full border ${getTrendColor()}`}>
                        {getTrendIcon()}
                        <span className="text-sm font-medium capitalize">{trend}</span>
                    </div>

                    {/* Audio Button */}
                    <button
                        onClick={speakPrice}
                        className="p-2 bg-primary-100 hover:bg-primary-200 rounded-full transition-colors"
                        title="Listen to price"
                    >
                        <Volume2 className="w-4 h-4 text-primary-600" />
                    </button>
                </div>
            </div>

            {/* Price */}
            <div className="mb-4">
                <div className="flex items-baseline space-x-2">
                    <span className="text-4xl font-bold text-primary-600">₹{price.toLocaleString()}</span>
                    <span className="text-lg text-gray-600">per {unit}</span>
                </div>

                {/* Confidence Level */}
                <div className="mt-2">
                    <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-600">Confidence:</span>
                        <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-32">
                            <div
                                className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${confidence * 100}%` }}
                            />
                        </div>
                        <span className="text-sm font-medium text-gray-700">
                            {Math.round(confidence * 100)}%
                        </span>
                    </div>
                </div>
            </div>

            {/* Details Toggle */}
            {(explanation || factors.length > 0) && (
                <div>
                    <button
                        onClick={() => setShowDetails(!showDetails)}
                        className="text-primary-600 hover:text-primary-700 text-sm font-medium mb-2"
                    >
                        {showDetails ? 'Hide Details' : 'Show Details'}
                    </button>

                    {showDetails && (
                        <div className="space-y-3">
                            {/* Explanation */}
                            {explanation && (
                                <div className="bg-blue-50 border border-blue-200 p-3 rounded-lg">
                                    <h4 className="text-sm font-semibold text-blue-900 mb-1">Price Analysis</h4>
                                    <p className="text-sm text-blue-800">{explanation}</p>
                                </div>
                            )}

                            {/* Factors */}
                            {factors.length > 0 && (
                                <div className="bg-gray-50 border border-gray-200 p-3 rounded-lg">
                                    <h4 className="text-sm font-semibold text-gray-900 mb-2">Price Factors</h4>
                                    <ul className="space-y-1">
                                        {factors.map((factor, index) => (
                                            <li key={index} className="text-sm text-gray-700 flex items-start">
                                                <span className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-2 flex-shrink-0" />
                                                {factor}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}