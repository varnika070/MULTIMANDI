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
    const [selectedLanguage, setSelectedLanguage] = useState('en-US')
    const [currentPriceData, setCurrentPriceData] = useState<PriceData | null>(null)
    const [isLoading, setIsLoading] = useState(false)

    const languages = [
        { code: 'en-US', name: 'English', flag: '🇺🇸' },
        { code: 'hi-IN', name: 'हिंदी', flag: '🇮🇳' },
        { code: 'te-IN', name: 'తెలుగు', flag: '🇮🇳' },
        { code: 'ta-IN', name: 'தமிழ்', flag: '🇮🇳' },
        { code: 'kn-IN', name: 'ಕನ್ನಡ', flag: '🇮🇳' }
    ]

    // Language-specific responses
    const getLocalizedResponse = (key: string, language: string, product?: string) => {
        const responses: Record<string, Record<string, string>> = {
            'en-US': {
                welcome: 'Welcome to OpenMandi! I can help you with price discovery and trading. Try saying "What is the price of rice?" or "I want to sell tomatoes".',
                priceHelp: `I can help you with prices! Which product are you interested in? I have data for rice, wheat, onion, potato, tomato, cotton, sugarcane, and turmeric.`,
                tradingHelp: 'Great! I can help you with trading. Let me know what product you want to trade and I\'ll provide current market prices and negotiation guidance.',
                negotiationHelp: 'I can help you analyze offers and provide negotiation advice. Tell me about the product, quantity, and price being discussed.',
                greeting: 'Hello! Welcome to OpenMandi. I\'m your AI trading assistant. I can help you with current market prices, trading advice, negotiation guidance, and connecting with buyers or sellers. What would you like to know?',
                generalHelp: 'I understand you\'re interested in agricultural trading. I can help with current prices, market trends, negotiation advice, and trading guidance. Try asking about specific products like "What is the price of rice?" or "I want to sell tomatoes".',
                priceInfo: `Here's the current market information for ${product}:`,
                dataError: `I couldn't find current price data for ${product}. Let me show you some sample data instead.`,
                systemError: 'Sorry, I\'m having trouble processing your request right now. Please try again.'
            },
            'hi-IN': {
                welcome: 'ओपनमंडी में आपका स्वागत है! मैं आपको मूल्य खोज और व्यापार में मदद कर सकता हूं। "चावल की कीमत क्या है?" या "मैं टमाटर बेचना चाहता हूं" कहने की कोशिश करें।',
                priceHelp: 'मैं आपको कीमतों के साथ मदद कर सकता हूं! आप किस उत्पाद में रुचि रखते हैं? मेरे पास चावल, गेहूं, प्याज, आलू, टमाटर, कपास, गन्ना और हल्दी का डेटा है।',
                tradingHelp: 'बहुत बढ़िया! मैं आपको व्यापार में मदद कर सकता हूं। मुझे बताएं कि आप कौन सा उत्पाद व्यापार करना चाहते हैं और मैं वर्तमान बाजार मूल्य और बातचीत मार्गदर्शन प्रदान करूंगा।',
                negotiationHelp: 'मैं आपको प्रस्तावों का विश्लेषण करने और बातचीत की सलाह देने में मदद कर सकता हूं। मुझे उत्पाद, मात्रा और कीमत के बारे में बताएं।',
                greeting: 'नमस्ते! ओपनमंडी में आपका स्वागत है। मैं आपका एआई ट्रेडिंग सहायक हूं। मैं वर्तमान बाजार मूल्य, व्यापारिक सलाह, बातचीत मार्गदर्शन और खरीदारों या विक्रेताओं से जुड़ने में मदद कर सकता हूं। आप क्या जानना चाहेंगे?',
                generalHelp: 'मैं समझता हूं कि आप कृषि व्यापार में रुचि रखते हैं। मैं वर्तमान कीमतों, बाजार के रुझान, बातचीत की सलाह और व्यापारिक मार्गदर्शन में मदद कर सकता हूं। "चावल की कीमत क्या है?" या "मैं टमाटर बेचना चाहता हूं" जैसे विशिष्ट उत्पादों के बारे में पूछने की कोशिश करें।',
                priceInfo: `यहाँ ${product} की वर्तमान बाजार जानकारी है:`,
                dataError: `मुझे ${product} के लिए वर्तमान मूल्य डेटा नहीं मिला। इसके बजाय मैं आपको कुछ नमूना डेटा दिखाता हूं।`,
                systemError: 'क्षमा करें, मुझे अभी आपके अनुरोध को संसाधित करने में परेशानी हो रही है। कृपया पुनः प्रयास करें।'
            },
            'ta-IN': {
                welcome: 'OpenMandi க்கு வரவேற்கிறோம்! நான் உங்களுக்கு விலை கண்டுபிடிப்பு மற்றும் வர்த்தகத்தில் உதவ முடியும். "அரிசியின் விலை என்ன?" அல்லது "நான் தக்காளி விற்க விரும்புகிறேன்" என்று சொல்லி முயற்சிக்கவும்.',
                priceHelp: 'நான் உங்களுக்கு விலைகளில் உதவ முடியும்! நீங்கள் எந்த தயாரிப்பில் ஆர்வமாக உள்ளீர்கள்? என்னிடம் அரிசி, கோதுமை, வெங்காயம், உருளைக்கிழங்கு, தக்காளி, பருத்தி, கரும்பு மற்றும் மஞ்சள் தரவு உள்ளது.',
                tradingHelp: 'அருமை! நான் உங்களுக்கு வர்த்தகத்தில் உதவ முடியும். நீங்கள் எந்த தயாரிப்பை வர்த்தகம் செய்ய விரும்புகிறீர்கள் என்று எனக்குத் தெரியப்படுத்துங்கள், நான் தற்போதைய சந்தை விலைகள் மற்றும் பேச்சுவார்த்தை வழிகாட்டுதலை வழங்குவேன்.',
                negotiationHelp: 'நான் உங்களுக்கு சலுகைகளை பகுப்பாய்வு செய்து பேச்சுவார்த்தை ஆலோசனை வழங்க உதவ முடியும். தயாரிப்பு, அளவு மற்றும் விலை பற்றி என்னிடம் சொல்லுங்கள்.',
                greeting: 'வணக்கம்! OpenMandi க்கு வரவேற்கிறோம். நான் உங்கள் AI வர்த்தக உதவியாளர். நான் தற்போதைய சந்தை விலைகள், வர்த்தக ஆலோசனை, பேச்சுவார்த்தை வழிகாட்டுதல் மற்றும் வாங்குபவர்கள் அல்லது விற்பவர்களுடன் இணைப்பதில் உதவ முடியும். நீங்கள் என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?',
                generalHelp: 'நீங்கள் விவசாய வர்த்தகத்தில் ஆர்வமாக உள்ளீர்கள் என்பதை நான் புரிந்துகொள்கிறேன். நான் தற்போதைய விலைகள், சந்தை போக்குகள், பேச்சுவார்த்தை ஆலோசனை மற்றும் வர்த்தக வழிகாட்டுதலில் உதவ முடியும். "அரிசியின் விலை என்ன?" அல்லது "நான் தக்காளி விற்க விரும்புகிறேன்" போன்ற குறிப்பிட்ட தயாரிப்புகளைப் பற்றி கேட்க முயற்சிக்கவும்.',
                priceInfo: `இதோ ${product} க்கான தற்போதைய சந்தை தகவல்:`,
                dataError: `${product} க்கான தற்போதைய விலை தரவை என்னால் கண்டுபிடிக்க முடியவில்லை. அதற்கு பதிலாக சில மாதிரி தரவை உங்களுக்குக் காட்டுகிறேன்.`,
                systemError: 'மன்னிக்கவும், உங்கள் கோரிக்கையை செயலாக்குவதில் எனக்கு இப்போது சிக்கல் உள்ளது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.'
            },
            'te-IN': {
                welcome: 'OpenMandi కి స్వాగతం! నేను మీకు ధర కనుగొనడం మరియు వ్యాపారంలో సహాయం చేయగలను. "బియ్యం ధర ఎంత?" లేదా "నేను టమోటాలు అమ్మాలని అనుకుంటున్నాను" అని చెప్పడానికి ప్రయత్నించండి.',
                priceHelp: 'నేను మీకు ధరలతో సహాయం చేయగలను! మీరు ఏ ఉత్పత్తిపై ఆసక్తి కలిగి ఉన్నారు? నా దగ్గర బియ్యం, గోధుమలు, ఉల్లిపాయలు, బంగాళాదుంపలు, టమోటాలు, పత్తి, చెరకు మరియు పసుపు డేటా ఉంది.',
                tradingHelp: 'గొప్ప! నేను మీకు వ్యాపారంలో సహాయం చేయగలను. మీరు ఏ ఉత్పత్తిని వ్యాపారం చేయాలనుకుంటున్నారో నాకు తెలియజేయండి మరియు నేను ప్రస్తుత మార్కెట్ ధరలు మరియు చర్చల మార్గదర్శకత్వం అందిస్తాను.',
                negotiationHelp: 'నేను మీకు ఆఫర్లను విశ్లేషించడంలో మరియు చర్చల సలహా అందించడంలో సహాయం చేయగలను. ఉత్పత్తి, పరిమాణం మరియు ధర గురించి నాకు చెప్పండి.',
                greeting: 'నమస్కారం! OpenMandi కి స్వాగతం. నేను మీ AI ట్రేడింగ్ అసిస్టెంట్. నేను ప్రస్తుత మార్కెట్ ధరలు, వ్యాపార సలహా, చర్చల మార్గదర్శకత్వం మరియు కొనుగోలుదారులు లేదా అమ్మకందారులతో కనెక్ట్ చేయడంలో సహాయం చేయగలను. మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?',
                generalHelp: 'మీరు వ్యవసాయ వ్యాపారంలో ఆసక్తి కలిగి ఉన్నారని నేను అర్థం చేసుకున్నాను. నేను ప్రస్తుత ధరలు, మార్కెట్ ట్రెండ్లు, చర్చల సలహా మరియు వ్యాపార మార్గదర్శకత్వంతో సహాయం చేయగలను. "బియ్యం ధర ఎంత?" లేదా "నేను టమోటాలు అమ్మాలనుకుంటున్నాను" వంటి నిర్దిష్ట ఉత్పత్తుల గురించి అడగడానికి ప్రయత్నించండి.',
                priceInfo: `ఇదిగో ${product} కోసం ప్రస్తుత మార్కెట్ సమాచారం:`,
                dataError: `${product} కోసం ప్రస్తుత ధర డేటాను నేను కనుగొనలేకపోయాను. బదులుగా నేను మీకు కొంత నమూనా డేటాను చూపిస్తాను.`,
                systemError: 'క్షమించండి, మీ అభ్యర్థనను ప్రాసెస్ చేయడంలో నాకు ఇప్పుడు ఇబ్బంది ఉంది. దయచేసి మళ్లీ ప్రయత్నించండి.'
            },
            'kn-IN': {
                welcome: 'OpenMandi ಗೆ ಸ್ವಾಗತ! ನಾನು ನಿಮಗೆ ಬೆಲೆ ಅನ್ವೇಷಣೆ ಮತ್ತು ವ್ಯಾಪಾರದಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಹುದು. "ಅಕ್ಕಿಯ ಬೆಲೆ ಎಷ್ಟು?" ಅಥವಾ "ನಾನು ಟೊಮೇಟೊಗಳನ್ನು ಮಾರಾಟ ಮಾಡಲು ಬಯಸುತ್ತೇನೆ" ಎಂದು ಹೇಳಲು ಪ್ರಯತ್ನಿಸಿ.',
                priceHelp: 'ನಾನು ನಿಮಗೆ ಬೆಲೆಗಳೊಂದಿಗೆ ಸಹಾಯ ಮಾಡಬಹುದು! ನೀವು ಯಾವ ಉತ್ಪನ್ನದಲ್ಲಿ ಆಸಕ್ತಿ ಹೊಂದಿದ್ದೀರಿ? ನನ್ನ ಬಳಿ ಅಕ್ಕಿ, ಗೋಧಿ, ಈರುಳ್ಳಿ, ಆಲೂಗಡ್ಡೆ, ಟೊಮೇಟೊ, ಹತ್ತಿ, ಕಬ್ಬು ಮತ್ತು ಅರಿಶಿನದ ಡೇಟಾ ಇದೆ.',
                tradingHelp: 'ಅದ್ಭುತ! ನಾನು ನಿಮಗೆ ವ್ಯಾಪಾರದಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಹುದು. ನೀವು ಯಾವ ಉತ್ಪನ್ನವನ್ನು ವ್ಯಾಪಾರ ಮಾಡಲು ಬಯಸುತ್ತೀರಿ ಎಂದು ನನಗೆ ತಿಳಿಸಿ ಮತ್ತು ನಾನು ಪ್ರಸ್ತುತ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು ಮತ್ತು ಮಾತುಕತೆ ಮಾರ್ಗದರ್ಶನವನ್ನು ಒದಗಿಸುತ್ತೇನೆ.',
                negotiationHelp: 'ನಾನು ನಿಮಗೆ ಆಫರ್‌ಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಮತ್ತು ಮಾತುಕತೆ ಸಲಹೆ ನೀಡಲು ಸಹಾಯ ಮಾಡಬಹುದು. ಉತ್ಪನ್ನ, ಪ್ರಮಾಣ ಮತ್ತು ಬೆಲೆಯ ಬಗ್ಗೆ ನನಗೆ ತಿಳಿಸಿ.',
                greeting: 'ನಮಸ್ಕಾರ! OpenMandi ಗೆ ಸ್ವಾಗತ. ನಾನು ನಿಮ್ಮ AI ಟ್ರೇಡಿಂಗ್ ಸಹಾಯಕ. ನಾನು ಪ್ರಸ್ತುತ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು, ವ್ಯಾಪಾರ ಸಲಹೆ, ಮಾತುಕತೆ ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ಖರೀದಿದಾರರು ಅಥವಾ ಮಾರಾಟಗಾರರೊಂದಿಗೆ ಸಂಪರ್ಕಿಸುವಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಹುದು. ನೀವು ಏನು ತಿಳಿದುಕೊಳ್ಳಲು ಬಯಸುತ್ತೀರಿ?',
                generalHelp: 'ನೀವು ಕೃಷಿ ವ್ಯಾಪಾರದಲ್ಲಿ ಆಸಕ್ತಿ ಹೊಂದಿದ್ದೀರಿ ಎಂದು ನಾನು ಅರ್ಥಮಾಡಿಕೊಂಡಿದ್ದೇನೆ. ನಾನು ಪ್ರಸ್ತುತ ಬೆಲೆಗಳು, ಮಾರುಕಟ್ಟೆ ಪ್ರವೃತ್ತಿಗಳು, ಮಾತುಕತೆ ಸಲಹೆ ಮತ್ತು ವ್ಯಾಪಾರ ಮಾರ್ಗದರ್ಶನದೊಂದಿಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. "ಅಕ್ಕಿಯ ಬೆಲೆ ಎಷ್ಟು?" ಅಥವಾ "ನಾನು ಟೊಮೇಟೊಗಳನ್ನು ಮಾರಾಟ ಮಾಡಲು ಬಯಸುತ್ತೇನೆ" ಮುಂತಾದ ನಿರ್ದಿಷ್ಟ ಉತ್ಪನ್ನಗಳ ಬಗ್ಗೆ ಕೇಳಲು ಪ್ರಯತ್ನಿಸಿ.',
                priceInfo: `ಇಲ್ಲಿ ${product} ಗಾಗಿ ಪ್ರಸ್ತುತ ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ:`,
                dataError: `${product} ಗಾಗಿ ಪ್ರಸ್ತುತ ಬೆಲೆ ಡೇಟಾವನ್ನು ನಾನು ಕಂಡುಹಿಡಿಯಲಾಗಲಿಲ್ಲ. ಬದಲಿಗೆ ನಾನು ನಿಮಗೆ ಕೆಲವು ಮಾದರಿ ಡೇಟಾವನ್ನು ತೋರಿಸುತ್ತೇನೆ.`,
                systemError: 'ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸುವಲ್ಲಿ ನನಗೆ ಇದೀಗ ತೊಂದರೆ ಇದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.'
            }
        }

        return responses[language]?.[key] || responses['en-US'][key] || key
    }

    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            type: 'system',
            content: 'Welcome to OpenMandi! I can help you with price discovery and trading.',
            timestamp: new Date()
        }
    ])

    // Update welcome message when language changes
    useEffect(() => {
        setMessages(prev => prev.map(msg =>
            msg.id === '1' ? { ...msg, content: getLocalizedResponse('welcome', selectedLanguage) } : msg
        ))
    }, [selectedLanguage])

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
                    addAIMessage(getLocalizedResponse('priceHelp', selectedLanguage))
                }
            } else if (lowerText.includes('sell') || lowerText.includes('buy')) {
                // Handle trading intent with negotiation assistance
                const products = ['rice', 'wheat', 'onion', 'potato', 'tomato', 'cotton', 'sugarcane', 'turmeric']
                const mentionedProduct = products.find(product => lowerText.includes(product))

                if (mentionedProduct) {
                    await fetchNegotiationAdvice(mentionedProduct, lowerText.includes('buy') ? 'buyer' : 'seller')
                } else {
                    addAIMessage(getLocalizedResponse('tradingHelp', selectedLanguage))
                }
            } else if (lowerText.includes('negotiate') || lowerText.includes('offer')) {
                addAIMessage(getLocalizedResponse('negotiationHelp', selectedLanguage))
            } else if (lowerText.includes('hello') || lowerText.includes('hi') || lowerText.includes('namaste')) {
                addAIMessage(getLocalizedResponse('greeting', selectedLanguage))
            } else {
                addAIMessage(getLocalizedResponse('generalHelp', selectedLanguage))
            }
        } catch (error) {
            addAIMessage(getLocalizedResponse('systemError', selectedLanguage))
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
                addAIMessage(getLocalizedResponse('priceInfo', selectedLanguage, product))
            } else {
                addAIMessage(getLocalizedResponse('dataError', selectedLanguage, product))

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
            addAIMessage(getLocalizedResponse('systemError', selectedLanguage))
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
                        <div className="flex items-center space-x-3">
                            <div className="text-sm text-gray-600 font-medium">
                                🌐 Active Language:
                            </div>
                            <select
                                value={selectedLanguage}
                                onChange={(e) => setSelectedLanguage(e.target.value)}
                                className="px-4 py-3 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white/90 backdrop-blur-sm shadow-sm font-medium"
                            >
                                {languages.map(lang => (
                                    <option key={lang.code} value={lang.code}>
                                        {lang.flag} {lang.name}
                                    </option>
                                ))}
                            </select>
                        </div>
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
                                language={selectedLanguage}
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
                                <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-xl p-4 border border-primary-100 mb-4">
                                    <p className="text-xs text-gray-600 font-medium">
                                        Try saying: "What is the price of rice?" or "I want to sell tomatoes"
                                    </p>
                                </div>
                                <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl p-3 border border-yellow-200">
                                    <p className="text-xs text-yellow-800 font-medium">
                                        🤖 Prototype AI - Responses demonstrate AI trading assistance flows
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