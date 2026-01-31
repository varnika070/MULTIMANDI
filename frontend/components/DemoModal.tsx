'use client'

import { useState, useEffect } from 'react'
import { X, Bot, TrendingUp, TrendingDown, Users, MapPin, Calendar, DollarSign } from 'lucide-react'

interface DemoModalProps {
    isOpen: boolean
    onClose: () => void
    action: 'buy' | 'sell'
    product: string
    price: number
    unit: string
    language: string
}

const translations = {
    'en-US': {
        buyTitle: 'AI Trading Assistant - Buy Order',
        sellTitle: 'AI Trading Assistant - Sell Order',
        buyExplanation: 'I can help you find the best buying opportunities for',
        sellExplanation: 'I can help you find the best selling opportunities for',
        marketAnalysis: 'Market Analysis',
        recommendations: 'AI Recommendations',
        nextSteps: 'Next Steps',
        close: 'Close',
        prototypeNote: '🤖 This is a prototype AI flow demonstration',
        buyRecommendations: [
            'Current price is favorable for buyers',
            'Quality suppliers available in your region',
            'Seasonal demand is moderate',
            'Consider bulk purchase for better rates'
        ],
        sellRecommendations: [
            'Market demand is strong for this product',
            'Price trend suggests good selling opportunity',
            'Multiple buyers active in your area',
            'Consider premium quality grading'
        ],
        buySteps: [
            'Connect with verified suppliers',
            'Negotiate quantity and delivery terms',
            'Arrange quality inspection',
            'Complete secure payment'
        ],
        sellSteps: [
            'List your product with quality details',
            'Set competitive pricing',
            'Connect with interested buyers',
            'Arrange pickup and payment'
        ]
    },
    'hi-IN': {
        buyTitle: 'एआई ट्रेडिंग सहायक - खरीद आदेश',
        sellTitle: 'एआई ट्रेडिंग सहायक - बिक्री आदेश',
        buyExplanation: 'मैं आपको सबसे अच्छे खरीदारी के अवसर खोजने में मदद कर सकता हूं',
        sellExplanation: 'मैं आपको सबसे अच्छे बिक्री के अवसर खोजने में मदद कर सकता हूं',
        marketAnalysis: 'बाजार विश्लेषण',
        recommendations: 'एआई सिफारिशें',
        nextSteps: 'अगले कदम',
        close: 'बंद करें',
        prototypeNote: '🤖 यह एक प्रोटोटाइप एआई फ्लो प्रदर्शन है',
        buyRecommendations: [
            'वर्तमान कीमत खरीदारों के लिए अनुकूल है',
            'आपके क्षेत्र में गुणवत्ता आपूर्तिकर्ता उपलब्ध हैं',
            'मौसमी मांग मध्यम है',
            'बेहतर दरों के लिए थोक खरीदारी पर विचार करें'
        ],
        sellRecommendations: [
            'इस उत्पाद के लिए बाजार की मांग मजबूत है',
            'कीमत की प्रवृत्ति अच्छे बिक्री अवसर का सुझाव देती है',
            'आपके क्षेत्र में कई खरीदार सक्रिय हैं',
            'प्रीमियम गुणवत्ता ग्रेडिंग पर विचार करें'
        ],
        buySteps: [
            'सत्यापित आपूर्तिकर्ताओं से जुड़ें',
            'मात्रा और डिलीवरी शर्तों पर बातचीत करें',
            'गुणवत्ता निरीक्षण की व्यवस्था करें',
            'सुरक्षित भुगतान पूरा करें'
        ],
        sellSteps: [
            'गुणवत्ता विवरण के साथ अपना उत्पाद सूचीबद्ध करें',
            'प्रतिस्पर्धी मूल्य निर्धारण सेट करें',
            'इच्छुक खरीदारों से जुड़ें',
            'पिकअप और भुगतान की व्यवस्था करें'
        ]
    },
    'ta-IN': {
        buyTitle: 'AI வர்த்தக உதவியாளர் - வாங்கும் ஆர்டர்',
        sellTitle: 'AI வர்த்தக உதவியாளர் - விற்பனை ஆர்டர்',
        buyExplanation: 'நான் உங்களுக்கு சிறந்த வாங்கும் வாய்ப்புகளைக் கண்டறிய உதவ முடியும்',
        sellExplanation: 'நான் உங்களுக்கு சிறந்த விற்பனை வாய்ப்புகளைக் கண்டறிய உதவ முடியும்',
        marketAnalysis: 'சந்தை பகுப்பாய்வு',
        recommendations: 'AI பரிந்துரைகள்',
        nextSteps: 'அடுத்த படிகள்',
        close: 'மூடு',
        prototypeNote: '🤖 இது ஒரு முன்மாதிரி AI ஓட்ட விளக்கம்',
        buyRecommendations: [
            'தற்போதைய விலை வாங்குபவர்களுக்கு சாதகமானது',
            'உங்கள் பகுதியில் தரமான சப்ளையர்கள் கிடைக்கின்றனர்',
            'பருவகால தேவை மிதமானது',
            'சிறந்த விலைகளுக்கு மொத்த வாங்குதலைக் கருத்தில் கொள்ளுங்கள்'
        ],
        sellRecommendations: [
            'இந்த தயாரிப்புக்கான சந்தை தேவை வலுவானது',
            'விலை போக்கு நல்ல விற்பனை வாய்ப்பை பரிந்துரைக்கிறது',
            'உங்கள் பகுதியில் பல வாங்குபவர்கள் செயலில் உள்ளனர்',
            'பிரீமியம் தர தரப்படுத்தலைக் கருத்தில் கொள்ளுங்கள்'
        ],
        buySteps: [
            'சரிபார்க்கப்பட்ட சப்ளையர்களுடன் இணைக்கவும்',
            'அளவு மற்றும் டெலிவரி விதிமுறைகளை பேச்சுவார்த்தை நடத்தவும்',
            'தர ஆய்வு ஏற்பாடு செய்யவும்',
            'பாதுகாப்பான கட்டணத்தை முடிக்கவும்'
        ],
        sellSteps: [
            'தர விவரங்களுடன் உங்கள் தயாரிப்பை பட்டியலிடுங்கள்',
            'போட்டி விலை நிர்ணயம் அமைக்கவும்',
            'ஆர்வமுள்ள வாங்குபவர்களுடன் இணைக்கவும்',
            'பிக்அப் மற்றும் கட்டணத்தை ஏற்பாடு செய்யவும்'
        ]
    },
    'te-IN': {
        buyTitle: 'AI ట్రేడింగ్ అసిస్టెంట్ - కొనుగోలు ఆర్డర్',
        sellTitle: 'AI ట్రేడింగ్ అసిస్టెంట్ - అమ్మకం ఆర్డర్',
        buyExplanation: 'నేను మీకు ఉత్తమ కొనుగోలు అవకాశాలను కనుగొనడంలో సహాయం చేయగలను',
        sellExplanation: 'నేను మీకు ఉత్తమ అమ్మకం అవకాశాలను కనుగొనడంలో సహాయం చేయగలను',
        marketAnalysis: 'మార్కెట్ విశ్లేషణ',
        recommendations: 'AI సిఫార్సులు',
        nextSteps: 'తదుపరి దశలు',
        close: 'మూసివేయండి',
        prototypeNote: '🤖 ఇది ప్రోటోటైప్ AI ఫ్లో ప్రదర్శన',
        buyRecommendations: [
            'ప్రస్తుత ధర కొనుగోలుదారులకు అనుకూలంగా ఉంది',
            'మీ ప్రాంతంలో నాణ్యమైన సరఫరాదారులు అందుబాటులో ఉన్నారు',
            'కాలానుగుణ డిమాండ్ మధ్యస్థంగా ఉంది',
            'మెరుగైన రేట్లకు బల్క్ కొనుగోలును పరిగణించండి'
        ],
        sellRecommendations: [
            'ఈ ఉత్పత్తికి మార్కెట్ డిమాండ్ బలంగా ఉంది',
            'ధర ధోరణి మంచి అమ్మకం అవకాశాన్ని సూచిస్తుంది',
            'మీ ప్రాంతంలో అనేక కొనుగోలుదారులు చురుకుగా ఉన్నారు',
            'ప్రీమియం నాణ్యత గ్రేడింగ్‌ను పరిగణించండి'
        ],
        buySteps: [
            'ధృవీకరించబడిన సరఫరాదారులతో కనెక్ట్ అవ్వండి',
            'పరిమాణం మరియు డెలివరీ నిబంధనలను చర్చించండి',
            'నాణ్యత తనిఖీని ఏర్పాటు చేయండి',
            'సురక్షిత చెల్లింపును పూర్తి చేయండి'
        ],
        sellSteps: [
            'నాణ్యత వివరాలతో మీ ఉత్పత్తిని జాబితా చేయండి',
            'పోటీ ధరలను సెట్ చేయండి',
            'ఆసక్తిగల కొనుగోలుదారులతో కనెక్ట్ అవ్వండి',
            'పికప్ మరియు చెల్లింపును ఏర్పాటు చేయండి'
        ]
    },
    'kn-IN': {
        buyTitle: 'AI ಟ್ರೇಡಿಂಗ್ ಸಹಾಯಕ - ಖರೀದಿ ಆದೇಶ',
        sellTitle: 'AI ಟ್ರೇಡಿಂಗ್ ಸಹಾಯಕ - ಮಾರಾಟ ಆದೇಶ',
        buyExplanation: 'ನಾನು ನಿಮಗೆ ಅತ್ಯುತ್ತಮ ಖರೀದಿ ಅವಕಾಶಗಳನ್ನು ಕಂಡುಹಿಡಿಯಲು ಸಹಾಯ ಮಾಡಬಹುದು',
        sellExplanation: 'ನಾನು ನಿಮಗೆ ಅತ್ಯುತ್ತಮ ಮಾರಾಟ ಅವಕಾಶಗಳನ್ನು ಕಂಡುಹಿಡಿಯಲು ಸಹಾಯ ಮಾಡಬಹುದು',
        marketAnalysis: 'ಮಾರುಕಟ್ಟೆ ವಿಶ್ಲೇಷಣೆ',
        recommendations: 'AI ಶಿಫಾರಸುಗಳು',
        nextSteps: 'ಮುಂದಿನ ಹಂತಗಳು',
        close: 'ಮುಚ್ಚಿ',
        prototypeNote: '🤖 ಇದು ಮೂಲಮಾದರಿ AI ಹರಿವಿನ ಪ್ರದರ್ಶನ',
        buyRecommendations: [
            'ಪ್ರಸ್ತುತ ಬೆಲೆ ಖರೀದಿದಾರರಿಗೆ ಅನುಕೂಲಕರವಾಗಿದೆ',
            'ನಿಮ್ಮ ಪ್ರದೇಶದಲ್ಲಿ ಗುಣಮಟ್ಟದ ಪೂರೈಕೆದಾರರು ಲಭ್ಯವಿದ್ದಾರೆ',
            'ಋತುಮಾನದ ಬೇಡಿಕೆ ಮಧ್ಯಮವಾಗಿದೆ',
            'ಉತ್ತಮ ದರಗಳಿಗಾಗಿ ಬೃಹತ್ ಖರೀದಿಯನ್ನು ಪರಿಗಣಿಸಿ'
        ],
        sellRecommendations: [
            'ಈ ಉತ್ಪನ್ನಕ್ಕೆ ಮಾರುಕಟ್ಟೆ ಬೇಡಿಕೆ ಬಲವಾಗಿದೆ',
            'ಬೆಲೆ ಪ್ರವೃತ್ತಿ ಉತ್ತಮ ಮಾರಾಟ ಅವಕಾಶವನ್ನು ಸೂಚಿಸುತ್ತದೆ',
            'ನಿಮ್ಮ ಪ್ರದೇಶದಲ್ಲಿ ಅನೇಕ ಖರೀದಿದಾರರು ಸಕ್ರಿಯರಾಗಿದ್ದಾರೆ',
            'ಪ್ರೀಮಿಯಂ ಗುಣಮಟ್ಟದ ಶ್ರೇಣೀಕರಣವನ್ನು ಪರಿಗಣಿಸಿ'
        ],
        buySteps: [
            'ಪರಿಶೀಲಿಸಿದ ಪೂರೈಕೆದಾರರೊಂದಿಗೆ ಸಂಪರ್ಕಿಸಿ',
            'ಪ್ರಮಾಣ ಮತ್ತು ವಿತರಣಾ ನಿಯಮಗಳನ್ನು ಮಾತುಕತೆ ಮಾಡಿ',
            'ಗುಣಮಟ್ಟದ ತಪಾಸಣೆಯನ್ನು ವ್ಯವಸ್ಥೆಗೊಳಿಸಿ',
            'ಸುರಕ್ಷಿತ ಪಾವತಿಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ'
        ],
        sellSteps: [
            'ಗುಣಮಟ್ಟದ ವಿವರಗಳೊಂದಿಗೆ ನಿಮ್ಮ ಉತ್ಪನ್ನವನ್ನು ಪಟ್ಟಿ ಮಾಡಿ',
            'ಸ್ಪರ್ಧಾತ್ಮಕ ಬೆಲೆ ನಿಗದಿಯನ್ನು ಹೊಂದಿಸಿ',
            'ಆಸಕ್ತ ಖರೀದಿದಾರರೊಂದಿಗೆ ಸಂಪರ್ಕಿಸಿ',
            'ಪಿಕಪ್ ಮತ್ತು ಪಾವತಿಯನ್ನು ವ್ಯವಸ್ಥೆಗೊಳಿಸಿ'
        ]
    }
}

export default function DemoModal({ isOpen, onClose, action, product, price, unit, language }: DemoModalProps) {
    const [isVisible, setIsVisible] = useState(false)

    const t = translations[language as keyof typeof translations] || translations['en-US']

    useEffect(() => {
        if (isOpen) {
            setIsVisible(true)
        }
    }, [isOpen])

    const handleClose = () => {
        setIsVisible(false)
        setTimeout(onClose, 300)
    }

    if (!isOpen) return null

    const recommendations = action === 'buy' ? t.buyRecommendations : t.sellRecommendations
    const steps = action === 'buy' ? t.buySteps : t.sellSteps

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className={`bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto transform transition-all duration-300 ${isVisible ? 'scale-100 opacity-100' : 'scale-95 opacity-0'
                }`}>
                {/* Header */}
                <div className={`${action === 'buy' ? 'bg-gradient-to-r from-emerald-500 to-emerald-600' : 'bg-gradient-to-r from-blue-500 to-blue-600'} px-6 py-4 rounded-t-2xl`}>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                                <Bot className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h2 className="text-xl font-bold text-white">
                                    {action === 'buy' ? t.buyTitle : t.sellTitle}
                                </h2>
                                <p className="text-white/80 text-sm">
                                    {action === 'buy' ? t.buyExplanation : t.sellExplanation} {product}
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={handleClose}
                            className="p-2 bg-white/20 rounded-xl hover:bg-white/30 transition-colors"
                        >
                            <X className="w-5 h-5 text-white" />
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="p-6 space-y-6">
                    {/* Prototype Notice */}
                    <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-xl p-4">
                        <p className="text-sm text-yellow-800 font-medium text-center">
                            {t.prototypeNote}
                        </p>
                    </div>

                    {/* Product Info */}
                    <div className="bg-gradient-to-r from-gray-50 to-slate-50 rounded-xl p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 capitalize">{product}</h3>
                                <p className="text-gray-600">Current Market Price</p>
                            </div>
                            <div className="text-right">
                                <div className="text-2xl font-bold text-gray-900">₹{price.toLocaleString()}</div>
                                <div className="text-sm text-gray-500">per {unit}</div>
                            </div>
                        </div>
                    </div>

                    {/* Market Analysis */}
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                            <MapPin className="w-5 h-5 text-blue-600" />
                            <span>{t.marketAnalysis}</span>
                        </h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                                <div className="flex items-center space-x-2 mb-2">
                                    <Users className="w-4 h-4 text-blue-600" />
                                    <span className="text-sm font-medium text-blue-900">Active Traders</span>
                                </div>
                                <div className="text-2xl font-bold text-blue-600">24</div>
                                <div className="text-xs text-blue-700">in your region</div>
                            </div>
                            <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                                <div className="flex items-center space-x-2 mb-2">
                                    <Calendar className="w-4 h-4 text-green-600" />
                                    <span className="text-sm font-medium text-green-900">Market Activity</span>
                                </div>
                                <div className="text-2xl font-bold text-green-600">High</div>
                                <div className="text-xs text-green-700">this week</div>
                            </div>
                        </div>
                    </div>

                    {/* AI Recommendations */}
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                            <Bot className="w-5 h-5 text-purple-600" />
                            <span>{t.recommendations}</span>
                        </h3>
                        <div className="space-y-3">
                            {recommendations.map((rec, index) => (
                                <div key={index} className="flex items-start space-x-3 p-3 bg-purple-50 border border-purple-200 rounded-xl">
                                    <div className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-white text-xs font-bold">{index + 1}</span>
                                    </div>
                                    <p className="text-sm text-purple-900">{rec}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Next Steps */}
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                            {action === 'buy' ? <TrendingUp className="w-5 h-5 text-emerald-600" /> : <TrendingDown className="w-5 h-5 text-blue-600" />}
                            <span>{t.nextSteps}</span>
                        </h3>
                        <div className="space-y-3">
                            {steps.map((step, index) => (
                                <div key={index} className={`flex items-start space-x-3 p-3 ${action === 'buy' ? 'bg-emerald-50 border-emerald-200' : 'bg-blue-50 border-blue-200'} border rounded-xl`}>
                                    <div className={`w-6 h-6 ${action === 'buy' ? 'bg-emerald-500' : 'bg-blue-500'} rounded-full flex items-center justify-center flex-shrink-0 mt-0.5`}>
                                        <span className="text-white text-xs font-bold">{index + 1}</span>
                                    </div>
                                    <p className={`text-sm ${action === 'buy' ? 'text-emerald-900' : 'text-blue-900'}`}>{step}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Close Button */}
                    <div className="flex justify-center pt-4">
                        <button
                            onClick={handleClose}
                            className={`px-8 py-3 ${action === 'buy' ? 'bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700' : 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700'} text-white rounded-xl font-medium transition-all duration-200 transform hover:scale-105`}
                        >
                            {t.close}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}