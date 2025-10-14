# Multiplayer Tic-Tac-Toe Game

A full-stack multiplayer Tic-Tac-Toe game built with Django REST Framework (backend) and React (frontend). Features server-authoritative game logic, real-time WebSocket communication, matchmaking system, and player leaderboard.

## 🚀 Features

- **Server-Authoritative Architecture**: All game logic runs on the server to prevent cheating
- **Real-Time Multiplayer**: WebSocket-based communication for instant game updates
- **Matchmaking System**: Automatic opponent pairing
- **Player Rating System**: Elo-based rating with wins/losses/draws tracking
- **Leaderboard**: Global ranking system
- **JWT Authentication**: Secure user authentication
- **Responsive Design**: Mobile-friendly UI
- **API Documentation**: Complete Swagger/OpenAPI documentation

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5.0.1 with Django REST Framework
- **Authentication**: JWT tokens with django-rest-framework-simplejwt
- **Real-Time**: Django Channels with Redis for WebSocket support
- **Database**: PostgreSQL (configurable)
- **Documentation**: drf-spectacular for OpenAPI/Swagger

### Frontend (React)
- **Framework**: React 18 with Vite
- **Routing**: React Router
- **State Management**: React Context API
- **Styling**: CSS Modules
- **HTTP Client**: Axios with interceptors
- **Notifications**: React Toastify

## 📋 Requirements Met

✅ **Server-authoritative multiplayer mode**: Game state managed entirely on server
✅ **Matchmaking mechanism**: Automatic pairing of waiting players
✅ **Multiple simultaneous games**: Redis-backed channel layers support concurrent games
✅ **Leaderboard system**: Player rankings with win/loss/draw statistics
✅ **Deployable solution**: Containerized and cloud-ready

## 🛠️ Tech Stack

### Backend
- Python 3.11+
- Django 5.0.1
- Django REST Framework 3.14.0
- Django Channels 0.7.0
- PostgreSQL
- Redis
- JWT Authentication

### Frontend
- Node.js 18+
- React 18
- Vite
- Axios
- React Router
- React Toastify

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose (recommended)
- Node.js 18+ and Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lila_games_assignment
   ```

2. **Environment Setup**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/schema/swagger-ui/

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🎮 How to Play

1. **Register/Login**: Create an account or log in
2. **Find Match**: Click "Play Now" to enter matchmaking
3. **Game Rules**:
   - Players take turns placing X's and O's
   - First to get 3 in a row (horizontally, vertically, or diagonally) wins
   - If board fills without winner, it's a draw
4. **Scoring**: Wins +25 rating, Losses -15 rating, Draws +5 rating

## 📚 API Documentation

Complete API documentation is available at `/api/schema/swagger-ui/` when the server is running.

### Key Endpoints

- `POST /api/v1/accounts/register/` - User registration
- `POST /api/v1/accounts/login/` - User login
- `POST /api/v1/games/matchmaking/` - Join matchmaking
- `GET /api/v1/games/{id}/` - Get game details
- `GET /api/v1/accounts/leaderboard/` - Get leaderboard
- `WS /ws/game/{game_id}/` - WebSocket game connection

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test game
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tic_tac_toe
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379
JWT_TOKEN_LIFETIME=24
JWT_REFRESH_TOKEN_LIFETIME=168
USER_THROTTLE_LIMIT=100/hour
ANON_THROTTLE_LIMIT=10/hour
CORS_ALLOWED_ORIGIN=http://localhost:5173
FRONTEND_URL=http://localhost:5173
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_API_WS_URL=ws://localhost:8000
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for free platforms like Railway, Render, or Heroku.

## 🏗️ Project Structure

```
├── backend/
│   ├── accounts/          # User management app
│   ├── game/             # Game logic and WebSocket consumers
│   ├── game_backend/     # Django project settings
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── contexts/     # React contexts
│   │   └── api/          # API clients
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🔒 Security Features

- JWT token authentication
- CORS protection
- Rate limiting on API endpoints
- Server-side game state validation
- Input sanitization
- Secure WebSocket connections

## 📈 Performance

- Redis-backed WebSocket channels for scalability
- Database query optimization with select_related
- Efficient matchmaking algorithm
- Compressed static files
- CDN-ready asset serving

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request


## 🙏 Acknowledgments

- Django Channels for WebSocket support
- React Toastify for notifications
- DRF Spectacular for API documentation
- The Django and React communities

---
