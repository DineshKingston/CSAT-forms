# ClientPulse Backend

Customer Satisfaction (CSAT) Feedback Collection and Analytics System - Backend API

## 🚀 Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Storage**: AWS S3
- **Deployment**: Docker + AWS ECR + EC2
- **CI/CD**: GitHub Actions
- **Web Server**: Nginx (reverse proxy)

## 📋 Features

- **Public Feedback Submission** - Anyone can submit CSAT feedback with optional screenshots
- **Admin Dashboard** - Secure analytics and reporting for administrators
- **JWT Authentication** - Secure token-based authentication
- **AWS S3 Integration** - Cloud storage for uploaded screenshots
- **Analytics API** - Comprehensive feedback metrics (30/60/90-day averages, rating distribution)
- **Export Reports** - Download feedback data as CSV or Excel
- **Health Monitoring** - `/health` endpoint for system status

## 🛠️ Local Development Setup

### Prerequisites

- Python 3.11+
- Poetry (dependency management)
- MySQL 8.0
- AWS Account (for S3)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/DineshKingston/CSAT-forms.git
cd CSAT-forms
```

2. **Install dependencies**
```bash
poetry install
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```bash
# Database
DB_ROOT_PASSWORD=your_db_password
DB_NAME=clientpulse

# JWT
JWT_SECRET_KEY=your-secret-key-here

# AWS S3
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET_NAME=your_bucket_name
AWS_REGION=ap-south-1

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://clientpulse.duckdns.org
```

4. **Run MySQL Database**
```bash
docker-compose up -d db
```

5. **Run the application**
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, access interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Public Endpoints
- `POST /api/feedback/` - Submit feedback (with optional screenshot)

#### Admin Endpoints (JWT Required)
- `POST /api/admin/register` - Create admin account
- `POST /api/admin/login` - Login and get JWT token
- `GET /api/admin/me` - Get current admin info
- `GET /api/analytics/reports` - Get analytics data
- `GET /api/analytics/download?format=csv|excel` - Download report

#### System
- `GET /health` - Health check endpoint

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t clientpulse-backend .
```

### Run with Docker Compose

```bash
docker-compose up -d
```

Services:
- **app**: FastAPI backend (port 8000)
- **db**: MySQL database (port 3306)
- **nginx**: Reverse proxy (ports 80, 443)

## 🚀 Production Deployment

### AWS ECR + EC2

The project includes automated CI/CD via GitHub Actions:

1. **Push to main branch** → Triggers deployment
2. **Build Docker image** → Uses Poetry for dependencies
3. **Push to ECR** → Stores image in AWS registry
4. **Deploy to EC2** → Pulls and runs latest image

### Manual Deployment

```bash
# Build and tag
docker build -t clientpulse-backend .
docker tag clientpulse-backend:latest ecr repositroy

# Push to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ecr rep
docker push ecr repo latest

# On EC2
docker-compose pull
docker-compose up -d
```

## 📁 Project Structure

```
clientpulse/
├── app/
│   ├── api/              # API route handlers
│   │   ├── admin.py      # Admin authentication
│   │   ├── analytics.py  # Analytics endpoints
│   │   └── feedback.py   # Feedback submission
│   ├── core/             # Core utilities
│   │   ├── s3.py         # AWS S3 integration
│   │   ├── security.py   # JWT & password hashing
│   │   └── dependencies.py # Auth dependencies
│   ├── models/           # SQLAlchemy ORM models
│   │   ├── admin.py      # Admin user model
│   │   └── feedback.py   # Feedback model
│   ├── schemas/          # Pydantic schemas
│   │   ├── admin.py      # Admin DTOs
│   │   ├── analytics.py  # Analytics DTOs
│   │   └── feedback.py   # Feedback DTOs
│   ├── config.py         # Configuration management
│   ├── database.py       # Database connection
│   └── main.py          # FastAPI application
├── nginx/
│   └── conf.d/
│       └── default.conf  # Nginx configuration
├── .github/
│   └── workflows/
│       └── deploy.yml    # CI/CD pipeline
├── docker-compose.yml    # Multi-container orchestration
├── Dockerfile           # Docker image definition
├── pyproject.toml       # Poetry dependencies
└── poetry.lock          # Locked dependency versions
```

## 🔐 Security

- **JWT Tokens**: 24-hour expiration
- **Password Hashing**: bcrypt with salt
- **HTTPS**: TLS 1.2+ via Let's Encrypt
- **CORS**: Configured origin whitelist
- **SQL Injection**: Protected via SQLAlchemy ORM
- **Secrets Management**: Environment variables + GitHub Secrets


