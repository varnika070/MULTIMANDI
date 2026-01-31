import Link from 'next/link'
import { Mic, Users, TrendingUp, Shield, MessageCircle, DollarSign, Sparkles, Globe, Award, ArrowRight } from 'lucide-react'

export default function HomePage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-blue-50 to-purple-50">
            {/* Header */}
            <header className="bg-white/80 backdrop-blur-md shadow-sm border-b border-white/20 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center py-4">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-blue-600 rounded-xl flex items-center justify-center">
                                <Sparkles className="w-6 h-6 text-white" />
                            </div>
                            <h1 className="text-2xl font-bold bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
                                OpenMandi
                            </h1>
                        </div>
                        <nav className="hidden md:block">
                            <div className="flex items-center space-x-6">
                                <Link href="/chat" className="text-gray-600 hover:text-emerald-600 px-4 py-2 rounded-full hover:bg-emerald-50 transition-all duration-200 font-medium">
                                    Start Trading
                                </Link>
                                <Link href="/prices" className="text-gray-600 hover:text-blue-600 px-4 py-2 rounded-full hover:bg-blue-50 transition-all duration-200 font-medium">
                                    Market Prices
                                </Link>
                                <Link href="/chat" className="bg-gradient-to-r from-emerald-500 to-blue-600 text-white px-6 py-2 rounded-full hover:shadow-lg transform hover:scale-105 transition-all duration-200 font-medium">
                                    Get Started
                                </Link>
                            </div>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="pt-16 pb-20 text-center">
                    {/* Badge */}
                    <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-emerald-100 to-blue-100 text-emerald-700 text-sm font-medium mb-8 border border-emerald-200">
                        <Award className="w-4 h-4 mr-2" />
                        AI-Powered Agricultural Trading Platform
                    </div>

                    <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 leading-tight">
                        <span className="block">Trade with</span>
                        <span className="block bg-gradient-to-r from-emerald-600 via-blue-600 to-purple-600 bg-clip-text text-transparent">
                            Your Voice
                        </span>
                    </h1>

                    <p className="mt-6 max-w-3xl mx-auto text-xl text-gray-600 leading-relaxed">
                        Connect with buyers and sellers using voice in your language. Get AI-powered price discovery,
                        fair negotiation assistance, and trade with confidence.
                    </p>

                    {/* Action Buttons */}
                    <div className="mt-12 flex flex-col sm:flex-row gap-6 justify-center items-center">
                        <Link href="/chat" className="group bg-gradient-to-r from-emerald-500 to-blue-600 text-white px-8 py-4 rounded-2xl text-lg font-semibold shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 flex items-center space-x-3 min-w-64">
                            <MessageCircle className="w-6 h-6" />
                            <span>Start Voice Trading</span>
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </Link>

                        <Link href="/prices" className="group bg-white/80 backdrop-blur-sm text-gray-700 px-8 py-4 rounded-2xl text-lg font-semibold border-2 border-gray-200 hover:border-emerald-300 hover:bg-emerald-50 transition-all duration-300 flex items-center space-x-3 min-w-64">
                            <DollarSign className="w-6 h-6 text-emerald-600" />
                            <span>Check Market Prices</span>
                        </Link>
                    </div>

                    {/* Stats */}
                    <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
                        <div className="text-center">
                            <div className="text-3xl font-bold text-emerald-600">8+</div>
                            <div className="text-gray-600 font-medium">Products</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-blue-600">6</div>
                            <div className="text-gray-600 font-medium">Languages</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-purple-600">24/7</div>
                            <div className="text-gray-600 font-medium">AI Assistant</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-orange-600">100%</div>
                            <div className="text-gray-600 font-medium">Fair Trading</div>
                        </div>
                    </div>
                </div>

                {/* Features Grid */}
                <div className="py-20">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">
                            Why Choose OpenMandi?
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Experience the future of agricultural trading with our advanced AI-powered platform
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <div className="group bg-white/60 backdrop-blur-sm p-8 rounded-3xl border border-white/20 hover:shadow-2xl hover:bg-white/80 transition-all duration-300 text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-emerald-400 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                                <Mic className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">Voice First</h3>
                            <p className="text-gray-600 leading-relaxed">
                                Speak naturally in your preferred language. No typing, no barriers - just natural conversation.
                            </p>
                        </div>

                        <div className="group bg-white/60 backdrop-blur-sm p-8 rounded-3xl border border-white/20 hover:shadow-2xl hover:bg-white/80 transition-all duration-300 text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                                <TrendingUp className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">Smart Pricing</h3>
                            <p className="text-gray-600 leading-relaxed">
                                AI analyzes market trends, seasonal factors, and quality grades for accurate price suggestions.
                            </p>
                        </div>

                        <div className="group bg-white/60 backdrop-blur-sm p-8 rounded-3xl border border-white/20 hover:shadow-2xl hover:bg-white/80 transition-all duration-300 text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                                <Users className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">Fair Negotiation</h3>
                            <p className="text-gray-600 leading-relaxed">
                                AI negotiation assistant ensures fair deals and protects against exploitation.
                            </p>
                        </div>

                        <div className="group bg-white/60 backdrop-blur-sm p-8 rounded-3xl border border-white/20 hover:shadow-2xl hover:bg-white/80 transition-all duration-300 text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                                <Shield className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">Secure & Private</h3>
                            <p className="text-gray-600 leading-relaxed">
                                Advanced security measures protect your data and ensure safe trading environment.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Language Support */}
                <div className="py-20 bg-gradient-to-r from-emerald-500/10 to-blue-500/10 rounded-3xl">
                    <div className="text-center mb-12">
                        <Globe className="w-16 h-16 text-emerald-600 mx-auto mb-6" />
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">
                            Speak Your Language
                        </h2>
                        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                            Trade comfortably in your native language with full support for regional dialects and agricultural terminology
                        </p>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 text-center">
                        {[
                            { name: 'English', native: 'English' },
                            { name: 'Hindi', native: 'हिंदी' },
                            { name: 'Telugu', native: 'తెలుగు' },
                            { name: 'Tamil', native: 'தமிழ்' },
                            { name: 'Kannada', native: 'ಕನ್ನಡ' },
                            { name: 'Malayalam', native: 'മലയാളം' }
                        ].map((lang, index) => (
                            <div key={index} className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl border border-white/20 hover:shadow-lg transition-all duration-200">
                                <div className="text-2xl font-bold text-gray-900 mb-1">{lang.native}</div>
                                <div className="text-sm text-gray-600">{lang.name}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* CTA Section */}
                <div className="py-20">
                    <div className="bg-gradient-to-r from-emerald-600 via-blue-600 to-purple-600 rounded-3xl shadow-2xl overflow-hidden relative">
                        <div className="absolute inset-0 bg-black/20"></div>
                        <div className="relative px-8 py-16 sm:px-16 text-center">
                            <h2 className="text-4xl font-bold text-white mb-6">
                                Ready to Transform Your Trading?
                            </h2>
                            <p className="text-xl text-white/90 mb-10 max-w-2xl mx-auto">
                                Join the future of agricultural trading. Fair prices, smart negotiations, and your voice at the center of it all.
                            </p>
                            <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                <Link href="/chat" className="group bg-white text-gray-900 px-8 py-4 rounded-2xl text-lg font-semibold hover:bg-gray-100 transition-all duration-300 flex items-center justify-center space-x-3 min-w-64">
                                    <Mic className="w-6 h-6" />
                                    <span>Start Trading Now</span>
                                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </Link>
                                <Link href="/prices" className="group bg-white/20 backdrop-blur-sm text-white px-8 py-4 rounded-2xl text-lg font-semibold border-2 border-white/30 hover:bg-white/30 transition-all duration-300 flex items-center justify-center space-x-3 min-w-64">
                                    <DollarSign className="w-6 h-6" />
                                    <span>Explore Prices</span>
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-gray-900 text-white">
                <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                    <div className="text-center">
                        <div className="flex items-center justify-center space-x-3 mb-4">
                            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-blue-600 rounded-lg flex items-center justify-center">
                                <Sparkles className="w-5 h-5 text-white" />
                            </div>
                            <span className="text-xl font-bold">OpenMandi</span>
                        </div>
                        <p className="text-gray-400 mb-4">
                            Empowering farmers and traders with AI-powered voice trading
                        </p>
                        <p className="text-sm text-gray-500">
                            © 2024 OpenMandi. Built with ❤️ for agricultural communities.
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    )
}