import Link from 'next/link'
import { Mic, Users, TrendingUp, Shield, MessageCircle, DollarSign } from 'lucide-react'

export default function HomePage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
            {/* Header */}
            <header className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center py-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <h1 className="text-2xl font-bold text-primary-600">OpenMandi</h1>
                            </div>
                        </div>
                        <nav className="hidden md:block">
                            <div className="ml-10 flex items-baseline space-x-4">
                                <Link href="/chat" className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                                    Start Trading
                                </Link>
                                <Link href="/prices" className="text-gray-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                                    Market Prices
                                </Link>
                            </div>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="text-center">
                    <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                        <span className="block">Voice-Based</span>
                        <span className="block text-primary-600">Agricultural Trading</span>
                    </h1>
                    <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
                        Connect with buyers and sellers using voice in your language. Get AI-powered price discovery and negotiation assistance.
                    </p>

                    {/* Large Action Buttons */}
                    <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
                        <Link href="/chat" className="btn-primary py-6 px-8 text-lg min-h-20 min-w-32 flex items-center justify-center space-x-3">
                            <MessageCircle className="w-6 h-6" />
                            <span className="font-semibold">Start Voice Chat</span>
                        </Link>

                        <Link href="/prices" className="btn-outline py-6 px-8 text-lg min-h-20 min-w-32 flex items-center justify-center space-x-3">
                            <DollarSign className="w-6 h-6" />
                            <span className="font-semibold">Check Prices</span>
                        </Link>
                    </div>
                </div>

                {/* Features */}
                <div className="mt-20">
                    <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
                        <div className="text-center">
                            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                                <Mic className="h-6 w-6" />
                            </div>
                            <h3 className="mt-6 text-lg font-medium text-gray-900">Voice Communication</h3>
                            <p className="mt-2 text-base text-gray-500">
                                Speak in your preferred language. No typing required.
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                                <TrendingUp className="h-6 w-6" />
                            </div>
                            <h3 className="mt-6 text-lg font-medium text-gray-900">Smart Pricing</h3>
                            <p className="mt-2 text-base text-gray-500">
                                AI-powered price discovery based on real mandi data.
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                                <Users className="h-6 w-6" />
                            </div>
                            <h3 className="mt-6 text-lg font-medium text-gray-900">Fair Negotiation</h3>
                            <p className="mt-2 text-base text-gray-500">
                                AI assistant helps ensure fair deals for everyone.
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                                <Shield className="h-6 w-6" />
                            </div>
                            <h3 className="mt-6 text-lg font-medium text-gray-900">Secure & Private</h3>
                            <p className="mt-2 text-base text-gray-500">
                                Your conversations and data are encrypted and protected.
                            </p>
                        </div>
                    </div>
                </div>

                {/* CTA Section */}
                <div className="mt-20 bg-primary-600 rounded-lg shadow-xl overflow-hidden">
                    <div className="px-6 py-12 sm:px-12 sm:py-16 lg:px-16">
                        <div className="text-center">
                            <h2 className="text-3xl font-extrabold text-white">
                                Ready to start trading?
                            </h2>
                            <p className="mt-4 text-lg text-primary-100">
                                Join thousands of farmers and traders using OpenMandi for fair, transparent agricultural trading.
                            </p>
                            <div className="mt-8">
                                <Link href="/chat" className="btn-secondary py-6 px-8 text-lg min-h-20 min-w-32 inline-flex items-center justify-center space-x-3">
                                    <Mic className="w-6 h-6" />
                                    <span className="font-semibold">Start Your First Trade</span>
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-white mt-20">
                <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                    <div className="text-center">
                        <p className="text-base text-gray-500">
                            © 2024 OpenMandi. Built for farmers, by farmers.
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    )
}