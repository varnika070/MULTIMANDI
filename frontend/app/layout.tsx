import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'OpenMandi - Voice-Based Agricultural Marketplace',
    description: 'Multilingual voice-based platform for agricultural trading with AI-powered price discovery and negotiation assistance',
    manifest: '/manifest.json',
    themeColor: '#22c55e',
    viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <div id="root">
                    {children}
                </div>
            </body>
        </html>
    )
}