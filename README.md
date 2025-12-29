# 🎓 University Recommendation Platform

A comprehensive AI-powered platform that guides students from major selection through university admission and scholarship applications.

## ✨ Features

### 🔐 User Authentication
- Phone number + OTP authentication (simulated)
- Email/password registration and login
- JWT token-based sessions
- Social auth infrastructure (Google/Apple - requires API keys)

### 🤖 AI Academic Guidance
- Personality and academic assessment tests
- AI-powered major recommendations (3-7 majors)
- Personalized study roadmaps
- Uses Ollama for local AI processing (with fallback to rule-based)

### 🏛️ University System
- Advanced university search with multiple filters
- AI-based recommendation engine
- University comparison tool (2-3 universities)
- Comprehensive university profiles with media
- Scholarship tracking system

### 📝 Application Management
- Full application lifecycle tracking
- Document upload and management
- Real-time status notifications
- Admin approval workflow

### 💰 Scholarship Module
- Scholarship search and filtering
- AI eligibility checking
- Application timeline and reminders
- Status tracking

### 🎁 Student Services
- Partner services (Cars, Banks, Telecom, Travel)
- Exclusive student offers and discounts
- Lead generation for partners

### 💳 Payment Integration
- Simulated payment gateway (KNET, Apple Pay, Card)
- Premium feature management
- Payment history tracking
- Refund processing

### 📱 Modern UI/UX
- Eye-appealing landing page with gradient animations
- Responsive design (mobile/tablet/desktop)
- Professional dashboard
- Smooth animations and transitions

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database
- **ChromaDB** - Vector database for AI embeddings
- **Ollama** - Local LLM runtime (llama3.2 or similar)
- **LangChain** - AI framework for chains and agents
- **LangGraph** - Stateful conversation management

### Frontend
- **HTML5/CSS3** - Modern semantic markup and styling
- **JavaScript (ES6+)** - Interactive frontend logic
- **Custom CSS** - No framework dependencies, pure CSS with gradients and animations

### Authentication & Security
- **JWT (JSON Web Tokens)** - Secure authentication
- **bcrypt** - Password hashing
- **python-jose** - JWT implementation

## 📦 Installation

### Prerequisites
1. Python 3.9+
2. Ollama (optional, for AI features)

### Install Ollama (Optional but Recommended)
```bash
# macOS
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2
```

### Setup

1. **Clone or navigate to the project directory:**
```bash
cd /Users/swarajsolanke/Smart_assistant_chatbot/university_recommander
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create environment file (optional):**
```bash
cp .env.example .env
# Edit .env with your configurations
```

4. **Initialize the database:**
```bash
cd backend
python database_enhanced.py
```

5. **Run the application:**
```bash
python main.py
```

The application will be available at:
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🚀 Quick Start

### First Time Setup

1. Start the server: `python backend/main.py`
2. Open http://localhost:8000 in your browser
3. Click "Get Started" to register
4. Complete your profile
5. Take the AI assessment (optional)
6. Get personalized university recommendations!

### Testing Authentication

**Phone OTP (Simulated):**
```bash
# Send OTP
POST /auth/send-otp
{"phone": "+1234567890"}

# Check console for OTP code
# Verify OTP
POST /auth/verify-otp
{"phone": "+1234567890", "otp_code": "123456"}
```

**Email/Password:**
```bash
POST /auth/register
{
  "email": "student@example.com",
  "password": "securepass123",
  "full_name": "John Doe"
}
```

### Testing University Search

```bash
GET /universities/search?country=Germany&scholarship_track=true&page=1
```

### Testing AI Recommendations

```bash
POST /universities/recommend
{
  "user_id": 1,
  "preferred_major": "Computer Science",
  "max_results": 10
}
```

## 📁 Project Structure

```
university_recommander/
├── backend/
│   ├── models/           # Pydantic data models
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   ├── middleware/       # Auth & security
│   ├── ai/              # AI prompts & embeddings
│   ├── graph/           # LangGraph chatbot
│   ├── utils/           # Helper functions
│   ├── database_enhanced.py  # Database schema
│   ├── config.py        # Configuration
│   ├── main.py          # Application entry
│   └── sqlite.py        # Database utilities
├── frontend/
│   └── static/
│       ├── css/         # Stylesheets
│       ├── js/          # JavaScript
│       └── templates/   # HTML pages
├── chroma_db/           # Vector database storage
├── storage/             # Uploaded files
├── chatbot.db           # SQLite database
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

Key environment variables (in `.env`):

```env
# Database
DATABASE_NAME=chatbot.db

# Security
SECRET_KEY=your-secret-jwt-key-here

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# SMS/OTP
SMS_PROVIDER=simulated  # or 'twilio'

# Payments
PAYMENT_MODE=simulated  # or 'live'

# Features
ENABLE_PREMIUM_FEATURES=true
ENABLE_SOCIAL_AUTH=true
```

## 📊 Database Schema

The platform includes 25+ tables:

- **Users & Profiles**: users, student_profiles, otp_verification, documents
- **Assessments**: assessment_tests, assessment_results, major_recommendations
- **Universities**: universities, majors, university_majors, university_media
- **Applications**: applications, application_documents
- **Scholarships**: scholarships, scholarship_applications
- **Services**: partners, service_offers, service_leads
- **Payments**: payments, premium_features
- **System**: notifications, chat_sessions, chat_messages, ai_weights

## 🎯 Key Features Explained

### AI Assessment System
The platform evaluates students across 6 dimensions:
1. Personality type
2. Academic strengths
3. Thinking style
4. Learning preferences
5. Interests
6. Career tendencies

Results are used to recommend 3-7 suitable majors with personalized roadmaps.

### University Recommendation Algorithm
Combines multiple factors:
- Student GPA (30%)
- Budget compatibility (25%)
- Scholarship availability (20%)
- Assessment results (15%)
- Country preference (10%)
- Historical success rates

### Simulated Services
For development/testing, the following are simulated:
- **SMS OTP**: Codes printed to console
- **Payment Gateway**: Simplified transaction flow
- **Social Auth**: Infrastructure ready, needs API keys

## 🔐 Security

- JWT tokens for authentication
- Password hashing with bcrypt
- SQL injection protection via parameterized queries
- File upload validation
- CORS configuration
- Rate limiting (infrastructure ready)

## 📱 API Endpoints

### Authentication
- `POST /auth/send-otp` - Send OTP
- `POST /auth/verify-otp` - Verify OTP & login
- `POST /auth/register` - Register new user
- `POST /auth/login` - Email/password login
- `GET /auth/me` - Get current user

### Universities
- `GET /universities/search` - Advanced search
- `GET /universities/{id}` - University details
- `POST /universities/recommend` - AI recommendations
- `POST /universities/compare` - Compare universities

### Applications
- `POST /application/apply` - Submit application
- `GET /application/my-applications` - User applications
- `PUT /application/{id}/status` - Update status (admin)

## 🚧 Production Deployment

### Required for Production:

1. **Change SECRET_KEY** in `.env`
2. **Configure real SMS provider** (Twilio, Nexmo)
3. **Set up payment gateway** (KNET, Stripe)
4. **Configure social auth** (Google/Apple OAuth)
5. **Use PostgreSQL** instead of SQLite
6. **Add HTTPS** with SSL certificates
7. **Set up proper CORS** origins
8. **Enable rate limiting**
9. **Configure email service**
10. **Set up monitoring & logging**

## 🤝 Contributing

This is a comprehensive platform with many areas for enhancement:
- Additional AI models and training
- More sophisticated matching algorithms
- Enhanced analytics dashboard
- Mobile app integration
- Multi-language support

## 📄 License

All rights reserved. This is a proprietary platform.

## 💬 Support

For issues or questions:
- Check API docs at `/docs`
- Review console logs for debugging
- Ensure Ollama is running for AI features
- Verify database initialization completed

## 🎉 Credits

Built with FastAPI, Ollama, LangChain, and modern web technologies.

---

**Version**: 1.0.0  
**Last Updated**: December 2025
