# ClientPulse - CSAT Feedback Collection System

![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20ECR%20%7C%20EC2-FF9900?logo=amazon-aws)

Production-ready **Customer Satisfaction (CSAT)** backend system for collecting feedback, storing screenshots in AWS S3, and providing analytics with JWT-protected admin dashboard.

## 🚀 Features

### Public Feedback API (No Authentication)
- Submit feedback with Name, Email, Rating (1-5), Description
- Optional screenshot upload to AWS S3
- Automatic client IP capture
- Timestamp auto-generation


### Admin Dashboard (JWT Protected)
- 🔐 Secure login with JWT authentication
- 📊 Analytics reports:
  - Total feedback count
  - Overall average rating
  - Average ratings (30, 60, 90 days)
  - Rating distribution (1-5 stars)
- 📥 Download reports (CSV/JSON)

### Infrastructure
- 🐳 Fully Dockerized (FastAPI + MySQL + Nginx)
- ☁️ AWS S3 for screenshot storage
- 🔄 CI/CD with GitHub Actions → AWS ECR → EC2
- 🌐 Nginx reverse proxy with HTTPS support
- 🔒 Production-ready security (bcrypt + JWT)

## 📋 Prerequisites

- Python 3.11+
- Poetry
- MySQL 8.0
- Docker & Docker Compose
- AWS Account (S3, ECR, EC2)
- Git

## 🛠️ Quick Start

### 1. Clone Repository

\`\`\`bash
git clone https://github.com/yourusername/clientpulse.git
cd clientpulse
\`\`\`

### 2. Install Dependencies

\`\`\`bash
# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
\`\`\`

### 3. Configure Environment

\`\`\`bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
\`\`\`

Required environment variables:
\`\`\`env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/clientpulse
JWT_SECRET_KEY=your-secret-key-change-this
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET_NAME=your-bucket-name
\`\`\`

### 4. Set Up Database

\`\`\`bash
# Start MySQL (if using Docker)
docker-compose up -d db

# Or use system MySQL
sudo service mysql start

# Create database
mysql -u root -p -e "CREATE DATABASE clientpulse;"
\`\`\`

### 5. Run Application

\`\`\`bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with Docker Compose
docker-compose up --build
\`\`\`

Visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### Public Endpoints

#### Submit Feedback
\`\`\`http
POST /api/feedback/
Content-Type: multipart/form-data

name: John Doe
email: john@example.com
rating: 5
description: Great service!
screenshot: [file]
\`\`\`

### Admin Endpoints

#### Register Admin
\`\`\`http
POST /api/admin/register
Content-Type: application/json

{
  "username": "admin",
  "email": "admin@example.com",
  "password": "securepassword"
}
\`\`\`

#### Login
\`\`\`http
POST /api/admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "securepassword"
}

Response: { "access_token": "...", "token_type": "bearer" }
\`\`\`

#### Get Analytics (Protected)
\`\`\`http
GET /api/analytics/reports
Authorization: Bearer <token>
\`\`\`

#### Download Report (Protected)
\`\`\`http
GET /api/analytics/download?format=csv
Authorization: Bearer <token>
\`\`\`

## 🐳 Docker Deployment

### Local Development
\`\`\`bash
docker-compose up --build
\`\`\`

### Production (EC2)
\`\`\`bash
# Build and push to ECR
docker build -t clientpulse .
docker tag clientpulse:latest <ecr-repo-url>:latest
docker push <ecr-repo-url>:latest

# On EC2 instance
docker pull <ecr-repo-url>:latest
docker run -d -p 8000:8000 --env-file .env clientpulse
\`\`\`

## 🔐 AWS Setup

### S3 Bucket
1. Create bucket: `clientpulse-screenshots`
2. Configure CORS and public read access (or use presigned URLs)
3. Add bucket policy for uploads

### ECR Repository
\`\`\`bash
aws ecr create-repository --repository-name clientpulse --region us-east-1
\`\`\`

### EC2 Instance
- **Type**: t2.micro (free tier eligible)
- **OS**: Ubuntu 22.04
- **Security Group**: Allow ports 22, 80, 443, 8000
- **Install**: Docker, AWS CLI

## ⚙️ GitHub Secrets

Configure these in **Settings → Secrets and variables → Actions**:

\`\`\`
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
ECR_REPOSITORY
EC2_HOST
EC2_SSH_KEY
DATABASE_URL
JWT_SECRET_KEY
AWS_S3_BUCKET_NAME
\`\`\`

## 🧪 Testing

\`\`\`bash
# Run tests
poetry run pytest

# API testing with curl
curl -X POST http://localhost:8000/api/feedback/ \
  -F "name=Test User" \
  -F "email=test@example.com" \
  -F "rating=5" \
  -F "description=Test feedback"
\`\`\`

## 📦 Project Structure

\`\`\`
clientpulse/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Security & S3
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── utils/            # Dependencies
│   ├── config.py         # Settings
│   ├── database.py       # DB connection
│   └── main.py           # FastAPI app
├── nginx/
│   └── nginx.conf        # Nginx config
├── .github/workflows/    # CI/CD
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml        # Poetry config
└── .env.example
\`\`\`

## 📊 Tech Stack

- **Backend**: FastAPI, Uvicorn
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Database**: MySQL 8.0
- **Authentication**: JWT (python-jose)
- **Password**: bcrypt (passlib)
- **Cloud**: AWS S3, ECR, EC2
- **DevOps**: Docker, GitHub Actions, Nginx
- **Environment**: Poetry, Python 3.11

## 🔄 CI/CD Pipeline

1. **Push to main** → Triggers GitHub Action
2. **Build Docker image** → Tag with commit SHA
3. **Push to ECR** → AWS Elastic Container Registry
4. **Deploy to EC2** → Pull latest image & restart
5. **Health check** → Verify deployment

## 🌐 HTTPS Setup (Bonus)

\`\`\`bash
# On EC2 instance
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
\`\`\`

## 📝 License

MIT License - feel free to use for learning and production!

## 👨‍💻 Author

**Dinesh Kingston**  
Assignment Project - Placibo Training

---

⭐ **Star this repo if you found it helpful!**
