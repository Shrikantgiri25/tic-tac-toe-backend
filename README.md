# Tic-Tac-Toe Backend

A Django-based backend API for a multiplayer Tic-Tac-Toe game with real-time WebSocket support, matchmaking, and player ratings.

## 🚀 Features

- **Server-Authoritative Game Logic**: All game state managed on the server to prevent cheating
- **Real-Time Multiplayer**: WebSocket communication using Django Channels
- **Matchmaking System**: Automatic pairing of waiting players
- **Player Rating System**: Elo-based rating with win/loss/draw tracking
- **JWT Authentication**: Secure user authentication with token-based auth
- **API Documentation**: Complete Swagger/OpenAPI documentation
- **PostgreSQL Database**: Robust data persistence
- **Redis Channel Layer**: Scalable WebSocket connections

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5.0.1 with Django REST Framework 3.14.0
- **Real-Time**: Django Channels 4.3.1 with Redis for WebSocket support
- **Database**: PostgreSQL with psycopg2-binary
- **Authentication**: JWT tokens with djangorestframework-simplejwt
- **Documentation**: drf-spectacular for OpenAPI/Swagger
- **CORS**: django-cors-headers for cross-origin requests
- **Deployment**: gunicorn and daphne for ASGI support

## 📋 Requirements Met

✅ **Server-authoritative multiplayer mode**: Game state managed entirely on server
✅ **Matchmaking mechanism**: Automatic pairing of waiting players
✅ **Multiple simultaneous games**: Redis-backed channel layers support concurrent games
✅ **Leaderboard system**: Player rankings with win/loss/draw statistics
✅ **Deployable solution**: Containerized and cloud-ready

## 🛠️ Tech Stack

- **Python**: 3.11+
- **Django**: 5.0.1
- **Django REST Framework**: 3.14.0
- **Django Channels**: 4.3.1
- **PostgreSQL**: Database
- **Redis**: Channel layer and caching
- **JWT Authentication**: Token-based auth
- **Gunicorn**: WSGI server
- **Daphne**: ASGI server for WebSockets

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- pip (Python package manager)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tic_tac_toe_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Environment Setup**
   ```bash
   cp backend/.env.example backend/.env
   # Edit .env with your database and Redis settings
   ```

5. **Database Setup**
   ```bash
   cd backend
   python manage.py migrate
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## 🎮 Game Features

- **Matchmaking**: Join matchmaking to find opponents automatically
- **Real-Time Gameplay**: WebSocket connections for instant game updates
- **Game Rules**:
  - Players take turns placing X's and O's
  - First to get 3 in a row (horizontally, vertically, or diagonally) wins
  - If board fills without winner, it's a draw
- **Scoring**: Wins +25 rating, Losses -15 rating, Draws +5 rating

## 📚 API Documentation

Complete API documentation is available at `/api/schema/swagger-ui/` when the server is running.

### Key Endpoints

#### Authentication
- `POST /api/v1/accounts/register/` - User registration
- `POST /api/v1/accounts/login/` - User login
- `GET /api/v1/accounts/leaderboard/` - Get leaderboard

#### Games
- `POST /api/v1/games/create/` - Create a new game
- `POST /api/v1/games/matchmaking/` - Join matchmaking
- `GET /api/v1/games/{id}/` - Get game details
- `GET /api/v1/games/my-games/` - Get user's games

#### WebSocket
- `WS /ws/game/{game_id}/` - Real-time game connection

## 🧪 Testing

Run the backend tests:
```bash
cd backend
python manage.py test
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tic_tac_toe
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379
JWT_TOKEN_LIFETIME=24
JWT_REFRESH_TOKEN_LIFETIME=168
USER_THROTTLE_LIMIT=1000/hour
ANON_THROTTLE_LIMIT=1000/hour
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend-domain.com
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

## 🚀 Deployment

### Using Docker (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

### Manual Deployment

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Run with Daphne (for WebSockets)**
   ```bash
   daphne game_backend.asgi:application --port 8000 --bind 0.0.0.0
   ```

## 🏗️ Project Structure

```
backend/
├── accounts/              # User management app
│   ├── migrations/        # Database migrations
│   ├── serializers/       # DRF serializers
│   ├── models.py          # User model
│   ├── views.py           # Authentication views
│   └── urls.py            # URL patterns
├── game/                  # Game logic app
│   ├── migrations/        # Database migrations
│   ├── consumers.py       # WebSocket consumers
│   ├── game_logic.py      # Game rules and validation
│   ├── models.py          # Game and Move models
│   ├── routing.py         # WebSocket routing
│   ├── serializer.py      # Game serializers
│   ├── tests.py           # Unit tests
│   ├── urls.py            # URL patterns
│   └── views.py           # Game API views
├── game_backend/          # Django project settings
│   ├── settings.py        # Main settings
│   ├── urls.py            # Root URL configuration
│   ├── asgi.py            # ASGI application
│   └── wsgi.py            # WSGI application
├── utils/                 # Utility functions
├── staticfiles/           # Collected static files
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🔒 Security Features

- JWT token authentication with refresh tokens
- CORS protection with configurable origins
- Rate limiting on API endpoints
- Server-side game state validation
- Input sanitization
- Secure WebSocket connections
- CSRF protection

## 📈 Performance

- Redis-backed WebSocket channels for scalability
- Database query optimization
- Efficient matchmaking algorithm
- Connection pooling for database
- Asynchronous WebSocket handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass (`python manage.py test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 🙏 Acknowledgments

- Django Channels for WebSocket support
- DRF Spectacular for API documentation
- The Django and DRF communities
- PostgreSQL for reliable data storage
- Redis for high-performance caching and channels

---

**Note**: This is the backend API only. The frontend application is maintained separately.
