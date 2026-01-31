'use client'

import { useState, useEffect } from 'react'
import { ArrowLeft, Send, Bot, User } from 'lucide-react'
import Link from 'next/link'
import VoiceInterface from '../../components/VoiceInterface'
import PriceDisplay from '../../components/PriceDisplay'
import BigButton from '../../components/BigButton'

interface Message {
    id: string
    type: 'user' | 'system' | 'ai'
    content: string
    timestamp: Date
    audioUrl?: string
}

interface PriceData {
    product: string
    price: number
    unit: string
    trend: 'up' | 'down' | 'stable'
    confidence: number
    explanation: string
    factors: string[]
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            type: 'system',
            content: 'Welcome to OpenMandi! I can help you with price discovery and trading. Try saying "What is the price of rice?" or "I want to sell tomatoes".',
            timestamp: new Date()
        }
    ])
    const [currentPriceData, setCurrentPriceData] = useState<PriceData | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [selectedLanguage, setSelectedLanguage] = useState('en-US')

    const languages = [
        { code: 'en-US', name: 'English' },
        { code: 'hi-IN', name: 'हिंदी' },
        { code: 'te-IN', name: 'తెలుగు' },
        { code: 'ta-IN', name: 'தமிழ்' },
        { code: 'kn-IN', name: 'ಕನ್ನಡ' }
    ]

    const handleVoiceTranscription = async (text: string) => {
        // Add user message
        const userMessage: Message = {
            id: Date.now().toString(),
            type: 'user',
            content: text,
            timestamp: new Date()
        }
        setMessages(prev => [...prev, userMessage])

        // Process the message
        await processUserMessage(text)
    }

    const processUserMessage = async (text: string) => {
        setIsLoading(true)

        try {
            // Simple keyword detection for demo
            const lowerText = text.toLowerCase()

            if (lowerText.includes('price') || lowerText.includes('cost') || lowerText.includes('rate')) {
                // Extract product name (simple approach)
                const products = ['rice', 'wheat', 'onion', 'potato', 'tomato', 'cotton', 'sugarcane', 'turmeric']
                const mentionedProduct = products.find(product => lowerText.includes(product))

                if (mentionedProduct) {
                    await fetchPriceData(mentionedProduct)
                } else {
                    addAIMessage("I can help you with prices! Which product are you interested in? I have data for rice, wheat, onion, potato, tomato, cotton, sugarcane, and turmeric.")
                }
            } else if (lowerText.includes('sell') || lowerText.includes('buy')) {
                // Handle trading intent with negotiation assistance
                const products = ['rice', 'wheat', 'onion', 'potato', 'tomato', 'cotton', 'sugarcane', 'turmeric']
                const mentionedProduct = products.find(product => lowerText.includes(product))

                if (mentionedProduct) {
                    await fetchNegotiationAdvice(mentionedProduct, lowerText.includes('buy') ? 'buyer' : 'seller')
                } else {
                    addAIMessage("Great! I can help you with trading. Let me know what product you want to trade and I'll provide current market prices and negotiation guidance.")
                }
            } else if (lowerText.includes('negotiate') || lowerText.includes('offer')) {
                addAIMessage("I can help you analyze offers and provide negotiation advice. Tell me about the product, quantity, and price being discussed.")
            } else if (lowerText.includes('hello') || lowerText.includes('hi') || lowerText.includes('namaste')) {
                addAIMessage("Hello! Welcome to OpenMandi. I'm your AI trading assistant. I can help you with current market prices, trading advice, negotiation guidance, and connecting with buyers or sellers. What would you like to know?")
            } else {
                addAIMessage("I understand you're interested in agricultural trading. I can help with current prices, market trends, negotiation advice, and trading guidance. Try asking about specific products like 'What is the price of rice?' or 'I want to sell tomatoes'.")
            }
        } catch (error) {
            addAIMessage("Sorry, I'm having trouble processing your request right now. Please try again.")
        } finally {
            setIsLoading(false)
        }
    }

    const fetchPriceData = async (product: string) => {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/price/suggestion/${product}`)
            if (response.ok) {
                const data = await response.json()

                const priceData: PriceData = {
                    product: data.product_name,
                    price: data.suggested_price,
                    unit: data.unit,
                    trend: Math.random() > 0.5 ? 'up' : 'down', // Random for demo
                    confidence: data.confidence_level,
                    explanation: data.explanation,
                    factors: data.factors
                }

                setCurrentPriceData(priceData)
                addAIMessage(`Here's the current market information for ${product}:`)
            } else {
                addAIMessage(`I couldn't find current price data for ${product}. Let me show you some sample data instead.`)

                // Fallback sample data
                const samplePrices: Record<string, PriceData> = {
                    rice: {
                        product: 'Rice',
                        price: 2500,
                        unit: 'quintal',
                        trend: 'up',
                        confidence: 0.85,
                        explanation: 'Rice prices are trending upward due to seasonal demand and good quality harvest.',
                        factors: ['Seasonal demand increase', 'Good harvest quality', 'Regional market conditions']
                    },
                    wheat: {
                        product: 'Wheat',
                        price: 2200,
                        unit: 'quintal',
                        trend: 'stable',
                        confidence: 0.90,
                        explanation: 'Wheat prices remain stable with consistent supply and demand balance.',
                        factors: ['Stable supply chain', 'Consistent demand', 'Government procurement']
                    }
                }

                setCurrentPriceData(samplePrices[product] || samplePrices.rice)
            }
        } catch (error) {
            console.error('Error fetching price data:', error)
            addAIMessage("I'm having trouble accessing current market data. Please try again later.")
        }
    }

    const addAIMessage = (content: string) => {
        const aiMessage: Message = {
            id: Date.now().toString(),
            type: 'ai',
            content,
            timestamp: new Date()
        }
        setMessages(prev => [...prev, aiMessage])
    }

    const fetchNegotiationAdvice = async (product: string, userRole: 'buyer' | 'seller') => {
        try {
            // Get market insights first
            const response = await fetch(`http://localhost:8000/api/v1/negotiation/market-insights/${product}`)
            if (response.ok) {
                const data = await response.json()

                const advice = `Here's negotiation guidance for ${product}:

📊 Market Range: ₹${data.market_data.range[0]} - ₹${data.market_data.range[1]} per ${data.market_data.unit}
💰 Average Price: ₹${data.market_data.base_price} per ${data.market_data.unit}

${userRole === 'buyer' ? '🛒 Buyer Tips:' : '🌾 Seller Tips:'}
${data.trading_tips.join('\n')}

Would you like me to analyze a specific offer or provide more detailed negotiation strategy?`

                addAIMessage(advice)
            } else {
                addAIMessage(`I can help you with ${userRole === 'buyer' ? 'buying' : 'selling'} ${product}. Let me know the quantity and price you're considering, and I'll provide negotiation advice.`)
            }
        } catch (error) {
            console.error('Error fetching negotiation advice:', error)
            addAIMessage(`I can help you with ${userRole === 'buyer' ? 'buying' : 'selling'} ${product}. Let me know more details about your trading needs.`)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
            {/* Header */}
            <header className="bg-white/80 backdrop-blur-md shadow-lg border-b border-white/20">
                <div className="max-w-4xl mx-auto px-4 py-6">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <Link href="/">
                                <BigButton
                                    icon={ArrowLeft}
                                    label="Back"
                                    onClick={() => { }}
                                    variant="outline"
                                    className="!min-w-auto !px-3"
                                />
                            </Link>
                            <div>
                                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                                    Voice Trading Chat
                                </h1>
                                <p className="text-sm text-gray-600 mt-1">AI-powered agricultural marketplace assistant</p>
                            </div>
                        </div>

                        {/* Language Selector */}
                        <select
                            value={selectedLanguage}
                            onChange={(e) => setSelectedLanguage(e.target.value)}
                            className="px-4 py-3 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white/90 backdrop-blur-sm shadow-sm"
                        >
                            {languages.map(lang => (
                                <option key={lang.code} value={lang.code}>{lang.name}</option>
                            ))}
                        </select>
                    </div>
                </div>
            </header>

            <div className="max-w-4xl mx-auto px-4 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Chat Area */}
                    <div className="lg:col-span-2">
                        <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-xl border border-white/20 h-96 flex flex-col overflow-hidden">
                            {/* Messages */}
                            <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-gradient-to-b from-white/50 to-white/80">
                                {messages.map((message) => (
                                    <div
                                        key={message.id}
                                        className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                                    >
                                        <div className={`message-bubble ${message.type} max-w-xs lg:max-w-md`}>
                                            <div className="flex items-start space-x-3">
                                                {message.type === 'ai' && (
                                                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center flex-shrink-0">
                                                        <Bot className="w-4 h-4 text-white" />
                                                    </div>
                                                )}
                                                {message.type === 'user' && (
                                                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center flex-shrink-0">
                                                        <User className="w-4 h-4 text-white" />
                                                    </div>
                                                )}
                                                <div className="flex-1">
                                                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                                                    <p className="text-xs opacity-70 mt-2">
                                                        {message.timestamp.toLocaleTimeString()}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}

                                {isLoading && (
                                    <div className="flex justify-start">
                                        <div className="bg-white/90 backdrop-blur-sm rounded-2xl px-6 py-4 shadow-lg border border-white/20">
                                            <div className="flex items-center space-x-3">
                                                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center">
                                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                                </div>
                                                <span className="text-sm text-gray-700">AI is thinking...</span>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Voice Interface */}
                        <div className="mt-8">
                            <VoiceInterface
                                onTranscription={handleVoiceTranscription}
                                language={selectedLanguage}
                            />
                        </div>
                    </div>

                    {/* Price Display Sidebar */}
                    <div className="lg:col-span-1">
                        {currentPriceData ? (
                            <PriceDisplay
                                product={currentPriceData.product}
                                price={currentPriceData.price}
                                unit={currentPriceData.unit}
                                trend={currentPriceData.trend}
                                confidence={currentPriceData.confidence}
                                explanation={currentPriceData.explanation}
                                factors={currentPriceData.factors}
                            />
                        ) : (
                            <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-xl border border-white/20 p-8 text-center">
                                <div className="w-16 h-16 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center mx-auto mb-6">
                                    <Bot className="w-8 h-8 text-white" />
                                </div>
                                <h3 className="text-xl font-semibold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent mb-3">
                                    AI Price Assistant
                                </h3>
                                <p className="text-gray-600 text-sm mb-6 leading-relaxed">
                                    Ask me about current market prices for agricultural products. I can provide real-time pricing, trends, and trading advice.
                                </p>
                                <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-xl p-4 border border-primary-100">
                                    <p className="text-xs text-gray-600 font-medium">
                                        Try saying: "What is the price of rice?" or "I want to sell tomatoes"
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}