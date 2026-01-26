import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import HomePage from '../app/page'

describe('HomePage', () => {
    it('renders the main heading', () => {
        render(<HomePage />)

        expect(screen.getByText('Voice-Based')).toBeInTheDocument()
        expect(screen.getByText('Agricultural Trading')).toBeInTheDocument()
    })

    it('renders the start trading button', () => {
        render(<HomePage />)

        const startTradingButton = screen.getByRole('link', { name: /start trading/i })
        expect(startTradingButton).toBeInTheDocument()
        expect(startTradingButton).toHaveAttribute('href', '/chat')
    })

    it('renders feature cards', () => {
        render(<HomePage />)

        expect(screen.getByText('Voice Communication')).toBeInTheDocument()
        expect(screen.getByText('Smart Pricing')).toBeInTheDocument()
        expect(screen.getByText('Fair Negotiation')).toBeInTheDocument()
        expect(screen.getByText('Secure & Private')).toBeInTheDocument()
    })

    it('has proper accessibility attributes', () => {
        render(<HomePage />)

        const mainHeading = screen.getByRole('heading', { level: 1 })
        expect(mainHeading).toBeInTheDocument()
    })
})