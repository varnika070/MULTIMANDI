'use client'

import { useState } from 'react'
import { TrendingUp, TrendingDown, Minus, Volume2, Star, Info, CheckCircle, AlertTriangle, Sparkles } from 'lucide-react'

interface PriceDisplayProps {
    product: string
    price: number
    unit: string
    trend: 'up' | 'down' | 'stable'
    confidence?: number
    explanation?: string
    factors?: string[]
    market?: string
    grade?: string
    updated_at?: string
}

export default function PriceDisplay({
    product,
    price,
    unit,
    trend,
    confidence = 0.85,
    explanation,
    factors = [],
    market,
    grade,
    updated_at
}: PriceDisplayProps) {
    const [showDetails, setShowDetails] = useState(false)

    const getTrendIcon = () => {
        switch (trend) {
            case 'up':
                return <TrendingUp className="w-5 h-5 text-emerald-500" />
            case 'down':
                return <TrendingDown className="w-5 h-5 text-red-500" />
            default:
                return <Minus className="w-5 h-5 text-gray-500" />
        }
    }

    const getTrendColor = () => {
        switch (trend) {
            case 'up':
                return 'text-emerald-600 bg-emerald-50 border-emerald-200'
            case 'down':
                return 'text-red-600 bg-red-50 border-red-200'
            default:
                return 'text-gray-600 bg-gray-50 border-gray-200'
        }
    }

    const getConfidenceColor = () => {
        if (confidence >= 0.8) return 'text-emerald-600 bg-emerald-100'
        if (confidence >= 0.6) return 'text-yellow-600 bg-yellow-100'
        return 'text-red-600 bg-red-100'
    }

    const getConfidenceIcon = () => {
        if (confidence >= 0.8) return <CheckCircle className="w-4 h-4" />
        if (confidence >= 0.6) return <AlertTriangle className="w-4 h-4" />
        return <AlertTriangle className="w-4 h-4" />
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
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-emerald-500 to-blue-600 px-6 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                            <Star className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-white capitalize">{product}</h3>
                            <p className="text-emerald-100 text-sm">Live Market Price</p>
                        </div>
                    </div>
                    <button
                        onClick={speakPrice}
                        className="p-2 bg-white/20 rounded-xl hover:bg-white/30 transition-colors group"
                        title="Listen to price"
                    >
                        <Volume2 className="w-5 h-5 text-white group-hover:scale-110 transition-transform" />
                    </button>
                </div>
            </div>

            {/* Price Display */}
            <div className="p-6">
                <div className="text-center mb-6">
                    <div className="flex items-center justify-center space-x-2 mb-2">
                        <span className="text-4xl font-bold text-gray-900">₹{price.toLocaleString()}</span>
                        <span className="text-lg text-gray-500">/{unit}</span>
                    </div>

                    {/* Trend Indicator */}
                    <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full border ${getTrendColor()}`}>
                        {getTrendIcon()}
                        <span className="text-sm font-medium capitalize">{trend} Trend</span>
                    </div>
                </div>

                {/* Market Info Cards */}
                <div className="grid grid-cols-2 gap-3 mb-6">
                    {market && (
                        <div className="bg-blue-50 border border-blue-200 rounded-xl p-3 text-center">
                            <div className="text-xs text-blue-600 font-medium mb-1">Market</div>
                            <div className="text-sm font-bold text-blue-900">{market}</div>
                        </div>
                    )}
                    {grade && (
                        <div className="bg-purple-50 border border-purple-200 rounded-xl p-3 text-center">
                            <div className="text-xs text-purple-600 font-medium mb-1">Quality</div>
                            <div className="text-sm font-bold text-purple-900">{grade}</div>
                        </div>
                    )}
                </div>

                {/* Confidence Score */}
                <div className="mb-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">Confidence Level</span>
                        <div className={`flex items-center space-x-1 px-2 py-1 rounded-full ${getConfidenceColor()}`}>
                            {getConfidenceIcon()}
                            <span className="text-sm font-bold">{Math.round(confidence * 100)}%</span>
                        </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                            className={`h-3 rounded-full transition-all duration-500 ${confidence >= 0.8 ? 'bg-gradient-to-r from-emerald-400 to-emerald-600' :
                                    confidence >= 0.6 ? 'bg-gradient-to-r from-yellow-400 to-yellow-600' :
                                        'bg-gradient-to-r from-red-400 to-red-600'
                                }`}
                            style={{ width: `${confidence * 100}%` }}
                        ></div>
                    </div>
                </div>

                {/* Details Section */}
                {(explanation || factors.length > 0) && (
                    <div className="mb-6">
                        <button
                            onClick={() => setShowDetails(!showDetails)}
                            className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium group"
                        >
                            <Info className="w-4 h-4 group-hover:scale-110 transition-transform" />
                            <span>{showDetails ? 'Hide Analysis' : 'Show Analysis'}</span>
                        </button>

                        {showDetails && (
                            <div className="mt-4 space-y-4">
                                {explanation && (
                                    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4">
                                        <div className="flex items-center space-x-2 mb-2">
                                            <Sparkles className="w-4 h-4 text-blue-600" />
                                            <h4 className="font-semibold text-blue-900">AI Market Analysis</h4>
                                        </div>
                                        <p className="text-blue-800 text-sm leading-relaxed">{explanation}</p>
                                    </div>
                                )}

                                {factors.length > 0 && (
                                    <div className="bg-gradient-to-r from-gray-50 to-slate-50 border border-gray-200 rounded-xl p-4">
                                        <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                                            <TrendingUp className="w-4 h-4 text-emerald-600" />
                                            <span>Key Price Factors</span>
                                        </h4>
                                        <div className="space-y-2">
                                            {factors.map((factor, index) => (
                                                <div key={index} className="flex items-start space-x-2">
                                                    <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></div>
                                                    <span className="text-sm text-gray-700">{factor}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}

                {/* Action Buttons */}
                <div className="grid grid-cols-2 gap-3 mb-4">
                    <button className="bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white px-4 py-3 rounded-xl font-medium transition-all duration-200 flex items-center justify-center space-x-2 group">
                        <TrendingUp className="w-4 h-4 group-hover:scale-110 transition-transform" />
                        <span>Buy Now</span>
                    </button>
                    <button className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-4 py-3 rounded-xl font-medium transition-all duration-200 flex items-center justify-center space-x-2 group">
                        <TrendingDown className="w-4 h-4 group-hover:scale-110 transition-transform" />
                        <span>Sell Now</span>
                    </button>
                </div>

                {/* Last Updated */}
                <div className="text-center">
                    <p className="text-xs text-gray-500">
                        {updated_at ? `Updated: ${updated_at}` : `Last updated: ${new Date().toLocaleTimeString()}`}
                    </p>
                </div>
            </div>
        </div>
    )
}