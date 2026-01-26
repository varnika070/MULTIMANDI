# OpenMandi

Voice-based multilingual agricultural marketplace that facilitates communication between buyers and sellers with AI-powered price discovery and negotiation assistance.

## Features

- 🎤 **Voice-First Interface**: Multilingual speech recognition and synthesis
- 🌍 **Multilingual Support**: Support for regional languages and dialects
- 💰 **AI Price Discovery**: Smart pricing based on mandi data analysis
- 🤝 **Negotiation Assistant**: AI-powered negotiation guidance
- 📱 **Low-Literacy Friendly**: Accessible UI design for all users
- ⚡ **Real-Time Chat**: WebSocket-based communication
- 🔒 **Secure**: End-to-end encryption and privacy controls

## Tech Stack

### Frontend
- **Next.js 14** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Socket.IO** for real-time communication
- **Vitest** for testing

### Backend
- **FastAPI** with Python 3.11
- **PostgreSQL** for data storage
- **Redis** for caching and sessions
- **SQLAlchemy** for ORM
- **Pytest** for testing

### AI Services
- **OpenAI Whisper** for speech recognition
- **Azure Cognitive Services** for text-to-speech
- **OpenAI GPT-4** for negotiation assistance

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker and Docker Compose

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd openmandi
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Or run locally**
   ```bash
   # Install dependencies
   npm install
   
   # Start services
   npm run dev
   ```

### Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Database Setup
```bash
# Start PostgreSQL and Redis
docker-compose up postgres redis -d

# Run database migrations (when available)
cd backend
alembic upgrade head
```

## Project Structure

```
openmandi/
├── frontend/                 # Next.js frontend
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities and configurations
│   ├── types/               # TypeScript type definitions
│   └── test/                # Frontend tests
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── schemas/        # Pydantic schemas
│   ├── tests/              # Backend tests
│   └── scripts/            # Database scripts
├── docker-compose.yml      # Docker services
└── README.md
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Frontend Tests
```bash
cd frontend
npm test                    # Run tests
npm run test:ui            # Run with UI
```

### Backend Tests
```bash
cd backend
pytest                     # Run all tests
pytest --cov              # Run with coverage
pytest -m property        # Run property-based tests only
```

## Development Commands

```bash
# Start all services
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Docker commands
npm run docker:build      # Build containers
npm run docker:up         # Start containers
npm run docker:down       # Stop containers
```

## Environment Variables

Key environment variables (see `.env.example`):

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `AZURE_SPEECH_KEY`: Azure Speech Services key
- `SECRET_KEY`: JWT secret key

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and tests
6. Submit a pull request

## License

This project is licensed under the MIT License.