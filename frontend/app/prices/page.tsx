'use client'

import { useState, useEffect } from 'react'
import { ArrowLeft, Search, Filter, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import Link from 'next/link'
import PriceDisplay from '../../components/PriceDisplay'
import BigButton from '../../components/BigButton'

interface PriceTrend {
    product: string
    current_price: number
    trend: 'up' | 'down' | 'stable'
    trend_symbol: string
    unit: string
    market?: string
    grade?: string
    updated_at?: string
}

export default function PricesPage() {
    const [priceData, setPriceData] = useState<Record<string, PriceTrend>>({})
    const [loading, setLoading] = useState(true)
    const [searchTerm, setSearchTerm] = useState('')
    const [selectedCategory, setSelectedCategory] = useState('all')

    const categories = [
        { value: 'all', label: 'All Products' },
        { value: 'grains', label: 'Grains' },
        { value: 'vegetables', label: 'Vegetables' },
        { value: 'cash_crops', label: 'Cash Crops' },
        { value: 'spices', label: 'Spices' }
    ]

    useEffect(() => {
        fetchPriceData()
    }, [])

    const fetchPriceData = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/price/trends')
            if (response.ok) {
                const data = await response.json()
                setPriceData(data)
            } else {
                // Fallback sample data
                setPriceData({
                    Rice: {
                        product: 'Rice',
                        current_price: 2500,
                        trend: 'up',
                        trend_symbol: '↑',
                        unit: 'quintal',
                        market: 'Koyambedu Wholesale Market',
                        grade: 'Grade A',
                        updated_at: '2 hours ago'
                    },
                    Wheat: {
                        product: 'Wheat',
                        current_price: 2200,
                        trend: 'down',
                        trend_symbol: '↓',
                        unit: 'quintal',
                        market: 'APMC Pune',
                        grade: 'FAQ',
                        updated_at: '3 hours ago'
                    },
                    Onion: {
                        product: 'Onion',
                        current_price: 3000,
                        trend: 'up',
                        trend_symbol: '↑',
                        unit: 'quintal',
                        market: 'Lasalgaon Mandi',
                        grade: 'Medium',
                        updated_at: '1 hour ago'
                    },
                    Potato: {
                        product: 'Potato',
                        current_price: 1800,
                        trend: 'stable',
                        trend_symbol: '→',
                        unit: 'quintal',
                        market: 'Agra Mandi',
                        grade: 'Grade A',
                        updated_at: 'Today'
                    },
                    Tomato: {
                        product: 'Tomato',
                        current_price: 4500,
                        trend: 'up',
                        trend_symbol: '↑',
                        unit: 'quintal',
                        market: 'Madurai Market',
                        grade: 'Hybrid',
                        updated_at: '30 minutes ago'
                    },
                    Cotton: {
                        product: 'Cotton',
                        current_price: 6200,
                        trend: 'down',
                        trend_symbol: '↓',
                        unit: 'quintal',
                        market: 'Warangal Cotton Market',
                        grade: 'Long Staple',
                        updated_at: 'Today'
                    },
                    Sugarcane: {
                        product: 'Sugarcane',
                        current_price: 350,
                        trend: 'stable',
                        trend_symbol: '→',
                        unit: 'quintal',
                        market: 'Kolhapur',
                        grade: 'Mill Grade',
                        updated_at: 'Yesterday'
                    },
                    Turmeric: {
                        product: 'Turmeric',
                        current_price: 12000,
                        trend: 'up',
                        trend_symbol: '↑',
                        unit: 'quintal',
                        market: 'Erode Turmeric Market',
                        grade: 'Finger Type',
                        updated_at: 'Today'
                    }
                })

            }
        } catch (error) {
            console.error('Error fetching price data:', error)
            // Use fallback data
            setPriceData({
                Rice: {
                    product: 'Rice',
                    current_price: 2500,
                    trend: 'up',
                    trend_symbol: '↑',
                    unit: 'quintal',
                    market: 'Koyambedu Wholesale Market',
                    grade: 'Grade A',
                    updated_at: '2 hours ago'
                },
                Wheat: {
                    product: 'Wheat',
                    current_price: 2200,
                    trend: 'down',
                    trend_symbol: '↓',
                    unit: 'quintal',
                    market: 'APMC Pune',
                    grade: 'FAQ',
                    updated_at: '3 hours ago'
                },
                Onion: {
                    product: 'Onion',
                    current_price: 3000,
                    trend: 'up',
                    trend_symbol: '↑',
                    unit: 'quintal',
                    market: 'Lasalgaon Mandi',
                    grade: 'Medium',
                    updated_at: '1 hour ago'
                },
                Potato: {
                    product: 'Potato',
                    current_price: 1800,
                    trend: 'stable',
                    trend_symbol: '→',
                    unit: 'quintal',
                    market: 'Agra Mandi',
                    grade: 'Grade A',
                    updated_at: 'Today'
                },
                Tomato: {
                    product: 'Tomato',
                    current_price: 4500,
                    trend: 'up',
                    trend_symbol: '↑',
                    unit: 'quintal',
                    market: 'Madurai Market',
                    grade: 'Hybrid',
                    updated_at: '30 minutes ago'
                },
                Cotton: {
                    product: 'Cotton',
                    current_price: 6200,
                    trend: 'down',
                    trend_symbol: '↓',
                    unit: 'quintal',
                    market: 'Warangal Cotton Market',
                    grade: 'Long Staple',
                    updated_at: 'Today'
                },
                Sugarcane: {
                    product: 'Sugarcane',
                    current_price: 350,
                    trend: 'stable',
                    trend_symbol: '→',
                    unit: 'quintal',
                    market: 'Kolhapur',
                    grade: 'Mill Grade',
                    updated_at: 'Yesterday'
                },
                Turmeric: {
                    product: 'Turmeric',
                    current_price: 12000,
                    trend: 'up',
                    trend_symbol: '↑',
                    unit: 'quintal',
                    market: 'Erode Turmeric Market',
                    grade: 'Finger Type',
                    updated_at: 'Today'
                }
            })

        } finally {
            setLoading(false)
        }
    }

    const filteredProducts = Object.entries(priceData).map(([productName, data]) => ({
        ...data,
        product: productName // Ensure product name is set correctly
    })).filter((item) => {
        const productName = item?.product ?? ''
        const query = searchTerm ?? ''

        return productName.toLowerCase().includes(query.toLowerCase())
    })


    const speakPriceOverview = () => {
        if ('speechSynthesis' in window) {
            const productCount = Object.keys(priceData).length
            const text = `Current market prices for ${productCount} agricultural products. Use the search to find specific products or ask me about any product.`
            const utterance = new SpeechSynthesisUtterance(text)
            utterance.rate = 0.9
            speechSynthesis.speak(utterance)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading market prices...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 py-4">
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
                                <h1 className="text-xl font-bold text-gray-900">Market Prices</h1>
                                <p className="text-sm text-gray-600">Real-time agricultural commodity prices</p>
                            </div>
                        </div>

                        <BigButton
                            icon={TrendingUp}
                            label="Listen to Overview"
                            audioLabel="Listen to market price overview"
                            onClick={speakPriceOverview}
                            variant="outline"
                        />
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto px-4 py-6">
                {/* Search and Filters */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <div className="flex flex-col sm:flex-row gap-4">
                        {/* Search */}
                        <div className="flex-1 relative">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                            <input
                                type="text"
                                placeholder="Search products (e.g., rice, wheat, onion)..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-lg"
                            />
                        </div>

                        {/* Category Filter */}
                        <div className="sm:w-48">
                            <select
                                value={selectedCategory}
                                onChange={(e) => setSelectedCategory(e.target.value)}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-lg"
                            >
                                {categories.map(category => (
                                    <option key={category.value} value={category.value}>
                                        {category.label}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>

                {/* Price Grid */}
                {filteredProducts.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredProducts.map((item) => (
                            <PriceDisplay
                                key={item.product}
                                product={item.product}
                                price={item.current_price}
                                unit={item.unit}
                                trend={item.trend}
                                confidence={0.85}
                                explanation={`Current market price for ${item.product} based on recent trading data and market conditions.`}
                                factors={[
                                    'Recent market transactions',
                                    'Seasonal demand patterns',
                                    'Supply chain conditions',
                                    'Regional price variations'
                                ]}
                            />
                        ))}
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow-md p-12 text-center">
                        <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                        <h3 className="text-xl font-medium text-gray-900 mb-2">No products found</h3>
                        <p className="text-gray-600 mb-6">
                            Try searching for products like rice, wheat, onion, potato, tomato, or cotton.
                        </p>
                        <BigButton
                            label="Clear Search"
                            onClick={() => setSearchTerm('')}
                            variant="outline"
                        />
                    </div>
                )}

                {/* Market Summary */}
                <div className="mt-8 bg-white rounded-lg shadow-md p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Market Summary</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div className="text-center p-4 bg-green-50 rounded-lg">
                            <TrendingUp className="w-8 h-8 text-green-600 mx-auto mb-2" />
                            <div className="text-2xl font-bold text-green-600">
                                {Object.values(priceData).filter(p => p.trend === 'up').length}
                            </div>
                            <div className="text-sm text-green-700">Products Trending Up</div>
                        </div>

                        <div className="text-center p-4 bg-red-50 rounded-lg">
                            <TrendingDown className="w-8 h-8 text-red-600 mx-auto mb-2" />
                            <div className="text-2xl font-bold text-red-600">
                                {Object.values(priceData).filter(p => p.trend === 'down').length}
                            </div>
                            <div className="text-sm text-red-700">Products Trending Down</div>
                        </div>

                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                            <Minus className="w-8 h-8 text-gray-600 mx-auto mb-2" />
                            <div className="text-2xl font-bold text-gray-600">
                                {Object.values(priceData).filter(p => p.trend === 'stable').length}
                            </div>
                            <div className="text-sm text-gray-700">Products Stable</div>
                        </div>
                    </div>
                </div>

                {/* Call to Action */}
                <div className="mt-8 bg-primary-600 rounded-lg shadow-md p-8 text-center">
                    <h2 className="text-2xl font-bold text-white mb-4">
                        Ready to Trade?
                    </h2>
                    <p className="text-primary-100 mb-6">
                        Start a voice conversation to get personalized trading advice and connect with buyers or sellers.
                    </p>
                    <Link href="/chat">
                        <BigButton
                            label="Start Voice Trading"
                            audioLabel="Start voice trading chat"
                            onClick={() => { }}
                            variant="secondary"
                            size="large"
                        />
                    </Link>
                </div>
            </div>
        </div>
    )
}