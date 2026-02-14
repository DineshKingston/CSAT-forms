    # ClientPulse CSAT - Complete Assignment Setup Guide

    **Project:** Customer Satisfaction Feedback System  
    **Tech Stack:** FastAPI + SQLAlchemy + Pydantic + MySQL  
    **Deployment:** AWS EC2 + S3 + ECR via GitHub Actions  
    **Deadline:** 16/02/2026 EOD

    ---

    ## 📋 Table of Contents

    1. [Local Development Setup](#1-local-development-setup)
    2. [Database Configuration](#2-database-configuration)
    3. [Application Development](#3-application-development)
    4. [Docker Containerization](#4-docker-containerization)
    5. [AWS Configuration](#5-aws-configuration)
    6. [EC2 Deployment](#6-ec2-deployment)
    7. [CI/CD Pipeline](#7-cicd-pipeline)
    8. [API Testing](#8-api-testing)
    9. [Deliverables](#9-deliverables)

    ---

    ## 1. Local Development Setup

    ### 1.1 Install Poetry (Virtual Environment)

    ```bash
    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 -

    # Add to PATH
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc

    # Verify installation
    poetry --version
    ```

    ### 1.2 Create Project

    ```bash
    # Navigate to your workspace
    cd ~/

    # Create project directory
    mkdir clientpulse && cd clientpulse

    # Initialize Poetry project
    poetry init --name="clientpulse" --python="^3.11" --no-interaction

    # Install dependencies
    poetry add fastapi uvicorn[standard] sqlalchemy pymysql alembic
    poetry add pydantic pydantic-settings python-jose[cryptography]
    poetry add passlib[bcrypt] boto3 python-multipart python-dotenv

    # Activate virtual environment
        poetry shell
    ```

    ### 1.3 Create Project Structure

    ```bash
    # Create directory structure
    mkdir -p app/{api,core,models,schemas,utils}
    touch app/__init__.py
    touch app/{main,config,database}.py
    touch app/api/__init__.py
    touch app/core/{__init__,security,s3}.py
    touch app/models/{__init__,feedback,admin}.py
    touch app/schemas/{__init__,feedback,admin,analytics}.py
    touch app/utils/{__init__,dependencies}.py

    # Create configuration files
    touch .env .env.example .gitignore
    touch Dockerfile docker-compose.yml
    touch README.md MANUAL_SETUP.md

    # Create Alembic for migrations
    alembic init alembic
    ```

    ---

    ## 2. Database Configuration

    ### 2.1 Install MySQL

    ```bash
    # Update system
    sudo apt update

    # Install MySQL Server
    sudo apt install mysql-server -y

    # Start MySQL service
    sudo service mysql start

    # Verify MySQL is running
    sudo service mysql status
    ```

    ### 2.2 Create Database

    ```bash
    # Login to MySQL
    mysql -u root -p
    # (Press Enter if no password is set initially)
    ```

    ```sql
    -- Create database
    CREATE DATABASE clientpulse;

    -- Create user (optional)
    CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'StrongPassword123!';

    -- Grant privileges
    GRANT ALL PRIVILEGES ON clientpulse.* TO 'appuser'@'localhost';
    FLUSH PRIVILEGES;

    -- Verify database
    SHOW DATABASES;

    -- Exit
    EXIT;
    ```

    ### 2.3 Configure Environment Variables

    **Create `.env` file:**
    ```bash
    nano .env
    ```

    **Add configuration:**
    ```env
    # Application
    ENVIRONMENT=development
    DEBUG=true

    # Database (Local Development)
    DATABASE_URL=mysql+pymysql://root:YourMySQLPassword@localhost:3306/clientpulse

    # JWT Authentication
    JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
    JWT_ALGORITHM=HS256
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

    # Security
    ALLOW_ADMIN_REGISTRATION=true

    # AWS S3 (Leave empty for local development)
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_REGION=us-east-1
    AWS_S3_BUCKET_NAME=

    # CORS
    CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
    ```

    ---

    ## 3. Application Development

    ### 3.1 Key Features Implementation

    ✅ **CRUD Operations** - All endpoints support Create, Read, Update, Delete
    ✅ **No-Auth Public API** - Feedback submission endpoint
    ✅ **JWT Authentication** - Admin login and protected routes
    ✅ **Client IP Capture** - Automatic IP logging
    ✅ **Screenshot Upload** - AWS S3 integration
    ✅ **Analytics Reporting** - 30/60/90 day averages
    ✅ **Rating Distribution** - Count of each rating (1-5)

    ### 3.2 Run Application Locally

    ```bash
    # Activate poetry environment
    poetry shell

    # Run with uvicorn
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

    # Access API documentation
    # Browser: http://localhost:8000/docs
    ```

    ### 3.3 Test Database Connection

    ```bash
    # Test health endpoint
    curl http://localhost:8000/health

    # Expected response:
    # {"status":"healthy","database":"connected","s3":"disabled"}
    ```

    ---

    ## 4. Docker Containerization

    ### 4.1 Create Dockerfile

    **File: `Dockerfile`**
    ```dockerfile
    FROM python:3.11-slim

    WORKDIR /app

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        && rm -rf /var/lib/apt/lists/*

    # Copy application code
    COPY ./app ./app

    # Install Python dependencies
    RUN pip install --no-cache-dir \
        fastapi==0.109.0 \
        uvicorn[standard]==0.27.0 \
        sqlalchemy==2.0.25 \
        pymysql==1.1.0 \
        alembic==1.13.1 \
        pydantic==2.5.3 \
        pydantic-settings==2.1.0 \
        python-jose[cryptography]==3.3.0 \
        passlib[bcrypt]==1.7.4 \
        boto3==1.34.34 \
        python-multipart==0.0.6 \
        python-dotenv==1.0.0

    EXPOSE 8000

    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

    ### 4.2 Create Docker Compose

    **File: `docker-compose.yml`**
    ```yaml
    version: '3.8'

    services:
    # MySQL Database
    db:
        image: mysql:8.0
        container_name: clientpulse_db
        restart: always
        environment:
        MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD:-rootpassword}
        MYSQL_DATABASE: ${DB_NAME:-clientpulse}
        ports:
        - "3306:3306"
        volumes:
        - mysql_data:/var/lib/mysql
        networks:
        - clientpulse_network
        healthcheck:
        test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
        interval: 10s
        timeout: 5s
        retries: 5

    # FastAPI Application  
    app:
        build:
        context: .
        dockerfile: Dockerfile
        container_name: clientpulse_app
        restart: always
        ports:
        - "8000:8000"
        environment:
        - DATABASE_URL=mysql+pymysql://root:${DB_ROOT_PASSWORD:-rootpassword}@db:3306/${DB_NAME:-clientpulse}
        - JWT_SECRET_KEY=${JWT_SECRET_KEY}
        - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
        - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
        - AWS_REGION=${AWS_REGION:-us-east-1}
        - AWS_S3_BUCKET_NAME=${AWS_S3_BUCKET_NAME}
        depends_on:
        db:
            condition: service_healthy
        networks:
        - clientpulse_network

    # Nginx Reverse Proxy
    nginx:
        image: nginx:alpine
        container_name: clientpulse_nginx
        restart: always
        ports:
        - "80:80"
        - "443:443"
        volumes:
        - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
        depends_on:
        - app
        networks:
        - clientpulse_network

    volumes:
    mysql_data:

    networks:
    clientpulse_network:
        driver: bridge
    ```

    ### 4.3 Run Docker Containers

    ```bash
    # Build and start all services
    docker-compose up --build

    # Run in detached mode (background)
    docker-compose up -d

    # View logs
    docker-compose logs -f app

    # Stop all services
    docker-compose down

    # Remove volumes (clears database)
    docker-compose down -v
    ```

    ---

    ## 5. AWS Configuration

    ### 5.1 Create AWS Account

    **Step-by-Step:**
    1. Go to https://aws.amazon.com
    2. Click **"Create an AWS Account"**
    3. Enter email address and choose account name
    4. Provide contact information
    5. Add payment method (credit/debit card required)
    6. Verify identity (phone verification)
    7. Choose **Basic Support Plan** (Free)
    8. Complete registration

    **After Registration:**
    - Verify email address
    - Login to AWS Management Console
    - Set up MFA (Multi-Factor Authentication) - Recommended

    ### 5.2 Create IAM User (Security Best Practice)

    **Do NOT use root account for daily operations!**

    ```
    1. AWS Console → IAM → Users → Add users
    2. User name: clientpulse-deployer
    3. Access type: ✓ Programmatic access
    4. Permissions: Attach existing policies
    ✓ AmazonEC2FullAccess
    ✓ AmazonS3FullAccess
    ✓ AmazonEC2ContainerRegistryFullAccess
    5. Create user
    6. Download CSV with Access Key ID and Secret Access Key
    ⚠️ SAVE THESE - You cannot retrieve them again!
    ```

    ### 5.3 Create S3 Bucket for Screenshots

    **Via AWS Console:**
    ```
    1. AWS Console → S3 → Create bucket
    2. Bucket name: clientpulse-screenshots
    (Must be globally unique)
    3. Region: us-east-1 (or your preferred region)
    4. Block Public Access settings:
    ✓ Uncheck "Block all public access"
    (We need public read for uploaded screenshots)
    5. Bucket Versioning: Disabled
    6. Encryption: Disabled (or enable if needed)
    7. Create bucket
    ```

    **Set Bucket Policy:**
    ```
    1. Select bucket → Permissions → Bucket Policy → Edit
    2. Add this policy:
    ```

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::clientpulse-screenshots/*"
        }
    ]
    }
    ```

    **Configure CORS:**
    ```
    1. Select bucket → Permissions → CORS → Edit
    2. Add this configuration:
    ```

    ```json
    [
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag"]
    }
    ]
    ```

    ### 5.4 Create ECR Repository (Docker Registry)

    **Via AWS Console:**
    ```
    1. AWS Console → ECR → Create repository
    2. Repository name: clientpulse
    3. Tag immutability: Disabled
    4. Scan on push: Enabled (optional)
    5. Encryption: AES-256
    6. Create repository
    7. Copy the repository URI (you'll need this later)
    Format: <account-id>.dkr.ecr.us-east-1.amazonaws.com/clientpulse
    ```

    **Via AWS CLI:**
    ```bash
    # Install AWS CLI first
    sudo apt install awscli -y

    # Configure AWS CLI
    aws configure
    # Enter:
    # - AWS Access Key ID
    # - AWS Secret Access Key
    # - Default region: us-east-1
    # - Default output format: json

    # Create ECR repository
    aws ecr create-repository --repository-name clientpulse --region us-east-1
    ```

    ### 5.5 Create EC2 Key Pair

    ```
    1. AWS Console → EC2 → Key Pairs → Create key pair
    2. Name: clientpulse-key
    3. Key pair type: RSA
    4. Private key file format: .pem
    5. Create key pair
    6. Download and save clientpulse-key.pem
    7. Move to safe location:
    mv ~/Downloads/clientpulse-key.pem ~/.ssh/
    chmod 400 ~/.ssh/clientpulse-key.pem
    ```

    ---

    ## 6. EC2 Deployment

    ### 6.1 Launch EC2 Instance

    **Step-by-Step:**
    ```
    1. AWS Console → EC2 → Launch Instance

    2. Name and tags:
    Name: ClientPulse-Production-Server

    3. Application and OS Images:
    ✓ Ubuntu Server 22.04 LTS (Free tier eligible)
    Architecture: 64-bit (x86)

    4. Instance type:
    ✓ t2.micro (Free tier eligible)
    1 vCPU, 1 GB RAM

    5. Key pair:
    ✓ Select: clientpulse-key (created earlier)

    6. Network settings:
    ✓ Allow SSH traffic from: My IP (or Anywhere for testing)
    ✓ Allow HTTP traffic from the internet
    ✓ Allow HTTPS traffic from the internet

    7. Configure storage:
    ✓ 8 GB gp3 (Free tier eligible)

    8. Advanced details (Optional):
    Leave as default

    9. Click "Launch instance"

    10. Wait for instance state: Running
    11. Copy the Public IPv4 address
    ```

    ### 6.2 Configure Security Group

    ```
    1. EC2 → Instances → Select your instance → Security → Security groups
    2. Click on the security group link
    3. Edit inbound rules → Add rules:

    Type            Protocol    Port Range    Source          Description
    SSH             TCP         22            My IP           SSH access
    HTTP            TCP         80            0.0.0.0/0       HTTP access
    HTTPS           TCP         443           0.0.0.0/0       HTTPS access
    Custom TCP      TCP         8000          0.0.0.0/0       FastAPI app
    MySQL/Aurora    TCP         3306          Security Group  DB access (optional)

    4. Save rules
    ```

    ### 6.3 Connect to EC2 Instance

    ```bash
    # Set correct permissions for key file
    chmod 400 ~/.ssh/clientpulse-key.pem

    # Connect via SSH
    ssh -i ~/.ssh/clientpulse-key.pem ubuntu@<EC2-PUBLIC-IP>

    # Accept fingerprint prompt (yes)
    ```

    ### 6.4 Setup EC2 Server

    **Once connected to EC2:**

    ```bash
    # Update system
    sudo apt update && sudo apt upgrade -y

    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu

    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Verify installations
    docker --version
    docker-compose --version

    # Install AWS CLI
    sudo apt install awscli -y

    # Configure AWS CLI (use IAM user credentials)
    aws configure
    # Enter your Access Key ID
    # Enter your Secret Access Key
    # Region: us-east-1
    # Format: json

    # Install Nginx
    sudo apt install nginx -y
    sudo systemctl enable nginx
    sudo systemctl start nginx

    # Logout and login again for docker group
    exit
    ssh -i ~/.ssh/clientpulse-key.pem ubuntu@<EC2-PUBLIC-IP>
    ```

    ### 6.5 Deploy Application on EC2

    ```bash
    # Create application directory
    mkdir -p ~/clientpulse
    cd ~/clientpulse

    # Create .env file
    nano .env
    ```

    **Add production environment variables:**
    ```env
    # Application
    ENVIRONMENT=production
    DEBUG=false

    # Database (Production)
    DATABASE_URL=mysql+pymysql://root:ProductionPassword123!@db:3306/clientpulse

    # JWT
    JWT_SECRET_KEY=your-production-secret-key-very-long-and-random
    JWT_ALGORITHM=HS256
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

    # Security
    ALLOW_ADMIN_REGISTRATION=false

    # AWS S3
    AWS_ACCESS_KEY_ID=your-aws-access-key-id
    AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
    AWS_REGION=us-east-1
    AWS_S3_BUCKET_NAME=clientpulse-screenshots

    # CORS (Add your frontend domain)
    CORS_ORIGINS=["http://<EC2-PUBLIC-IP>","https://yourdomain.com"]
    ```

    **Pull and run Docker image:**
    ```bash
    # Login to ECR
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-ecr-uri>

    # Pull image (after pushing from GitHub Actions)
    docker pull <ecr-uri>/clientpulse:latest

    # Run container
    docker run -d \
    --name clientpulse_app \
    --restart always \
    -p 8000:8000 \
    --env-file .env \
    <ecr-uri>/clientpulse:latest

    # Check logs
    docker logs -f clientpulse_app
    ```

    ### 6.6 Configure Nginx as Reverse Proxy

    ```bash
    # Create Nginx configuration
    sudo nano /etc/nginx/sites-available/clientpulse
    ```

    **Add configuration:**
    ```nginx
    server {
        listen 80;
        server_name <EC2-PUBLIC-IP>;

        # Increase client max body size for file uploads
        client_max_body_size 10M;

        location / {
            proxy_pass http://localhost:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }
    }
    ```

    **Enable site:**
    ```bash
    # Create symbolic link
    sudo ln -s /etc/nginx/sites-available/clientpulse /etc/nginx/sites-enabled/

    # Remove default site
    sudo rm /etc/nginx/sites-enabled/default

    # Test configuration
    sudo nginx -t

    # Reload Nginx
    sudo systemctl reload nginx

    # Check status
    sudo systemctl status nginx
    ```

    ### 6.7 Verify Deployment

    ```bash
    # Test from EC2
    curl http://localhost:8000/health

    # Test from your local machine
    curl http://<EC2-PUBLIC-IP>/health

    # Access API docs
    # Browser: http://<EC2-PUBLIC-IP>/docs
    ```

    ---

    ## 7. CI/CD Pipeline

    ### 7.1 Configure GitHub Secrets

    ```
    Repository → Settings → Secrets and variables → Actions → New repository secret

    Add these secrets:
    ┌──────────────────────────┬────────────────────────────────────┐
    │ Secret Name              │ Value                              │
    ├──────────────────────────┼────────────────────────────────────┤
    │ AWS_ACCESS_KEY_ID        │ <Your IAM Access Key>              │
    │ AWS_SECRET_ACCESS_KEY    │ <Your IAM Secret Key>              │
    │ AWS_REGION               │ us-east-1                          │
    │ ECR_REPOSITORY           │ clientpulse                        │
    │ EC2_HOST                 │ <EC2 Public IP>                    │
    │ EC2_USER                 │ ubuntu                             │
    │ EC2_SSH_KEY              │ <Content of clientpulse-key.pem>   │
    │ DATABASE_URL             │ mysql+pymysql://...                │
    │ JWT_SECRET_KEY           │ <Your production secret>           │
    │ AWS_S3_BUCKET_NAME       │ clientpulse-screenshots            │
    └──────────────────────────┴────────────────────────────────────┘
    ```

    ### 7.2 Create GitHub Actions Workflow

    **File: `.github/workflows/deploy.yml`** (Already exists in your project)

    ### 7.3 Push Code to GitHub

    ```bash
    # Initialize git (if not already done)
    git init

    # Add files
    git add .

    # Commit
    git commit -m "Complete ClientPulse CSAT implementation"

    # Add remote (replace with your repo URL)
    git remote add origin https://github.com/yourusername/clientpulse.git

    # Push to main branch (triggers deployment)
    git push -u origin main
    ```

    ### 7.4 Monitor Deployment

    ```
    1. GitHub → Your Repository → Actions
    2. Click on the latest workflow run
    3. Monitor each step:
    - Checkout code
    - Configure AWS credentials
    - Login to ECR
    - Build and push Docker image
    - Deploy to EC2
    - Verify deployment
    4. Check for green checkmarks ✅
    ```

    ---

    ## 8. API Testing

    ### 8.1 Import Postman Collection

    ```
    1. Open Postman
    2. File → Import
    3. Select: ClientPulse_API.postman_collection.json
    4. Create environment: Production
    5. Add variable: base_url = http://<EC2-PUBLIC-IP>
    ```

    ### 8.2 Test All Endpoints

    **1. Health Check**
    ```
    GET {{base_url}}/health
    Expected: {"status":"healthy","database":"connected","s3":"enabled"}
    ```

    **2. Submit Feedback (Public - No Auth)**
    ```
    POST {{base_url}}/api/feedback/
    Body (form-data):
    - name: John Doe
    - email: john@example.com
    - rating: 5
    - description: Great service!
    - screenshot: [upload file]

    Response: 201 Created
    ```

    **3. Register First Admin**
    ```
    POST {{base_url}}/api/admin/register
    Body (JSON):
    {
    "username": "admin",
    "email": "admin@clientpulse.com",
    "password": "SecurePass123!"
    }

    Response: 201 Created
    ```

    **4. Admin Login**
    ```
    POST {{base_url}}/api/admin/login
    Body (JSON):
    {
    "username": "admin",
    "password": "SecurePass123!"
    }

    Response: 200 OK
    {
    "access_token": "eyJ...",
    "token_type": "bearer"
    }

    Save the token for next requests!
    ```

    **5. Get Analytics Report (Protected)**
    ```
    GET {{base_url}}/api/analytics/reports
    Headers:
    Authorization: Bearer <your-token>

    Response: 200 OK
    {
    "total_feedbacks": 10,
    "overall_avg_rating": 4.5,
    "avg_rating_last_30_days": 4.7,
    "avg_rating_last_60_days": 4.6,
    "avg_rating_last_90_days": 4.5,
    "rating_distribution": {
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4
    }
    }
    ```

    **6. Download CSV Report (Protected)**
    ```
    GET {{base_url}}/api/analytics/download?format=csv
    Headers:
    Authorization: Bearer <your-token>

    Response: 200 OK (Downloads feedbacks.csv)
    ```

    **7. Download JSON Report (Protected)**
    ```
    GET {{base_url}}/api/analytics/download?format=json
    Headers:
    Authorization: Bearer <your-token>

    Response: 200 OK (Downloads feedbacks.json)
    ```

    ---

    ## 9. Deliverables

    ### 9.1 Checklist

    ✅ **Git Repository**
    - Complete source code
    - README.md with setup instructions
    - .env.example with all required variables
    - .gitignore properly configured

    ✅ **Postman Collection**
    - ClientPulse_API.postman_collection.json
    - All endpoints documented
    - Environment variables configured

    ✅ **Deployment URL**
    - Public EC2 instance accessible
    - Health check endpoint working
    - API documentation available at /docs

    ✅ **Docker Setup**
    - Dockerfile optimized for production
    - docker-compose.yml with all services
    - Multi-container setup (app + db + nginx)

    ✅ **CI/CD Pipeline**
    - GitHub Actions workflow configured
    - Automated deployment on push to main
    - ECR integration for Docker images

    ✅ **AWS Integration**
    - S3 bucket for screenshot storage
    - EC2 instance for hosting
    - ECR for Docker registry
    - IAM user with proper permissions

    ✅ **Documentation**
    - MANUAL_SETUP.md
    - COMPLETE_SETUP_GUIDE.md
    - README.md
    - API documentation via FastAPI /docs

    ---

    ## 🎯 Quick Reference Commands

    ### Local Development
    ```bash
    poetry shell                                    # Activate environment
    uvicorn app.main:app --reload                  # Run app
    docker-compose up -d                           # Run with Docker
    ```

    ### AWS Operations
    ```bash
    aws configure                                   # Setup credentials
    aws s3 ls s3://clientpulse-screenshots        # List S3 files
    aws ecr get-login-password | docker login...  # Login to ECR
    ```

    ### EC2 Management
    ```bash
    ssh -i ~/.ssh/clientpulse-key.pem ubuntu@<IP> # Connect
    docker logs -f clientpulse_app                 # View logs
    docker restart clientpulse_app                 # Restart app
    sudo systemctl status nginx                    # Check Nginx
    ```

    ### GitHub Actions
    ```bash
    git add .                                      # Stage changes
    git commit -m "Update feature"                 # Commit
    git push origin main                          # Deploy!
    ```

    ---

    ## 🚨 Common Issues & Solutions

    ### Issue 1: S3 Upload Fails
    ```bash
    # Check AWS credentials
    aws s3 ls

    # Verify bucket permissions
    aws s3api get-bucket-policy --bucket clientpulse-screenshots

    # Test upload
    aws s3 cp test.txt s3://clientpulse-screenshots/
    ```

    ### Issue 2: EC2 Connection Refused
    ```bash
    # Check security group allows ports 22, 80, 443, 8000
    # Check application is running
    docker ps

    # Check Nginx status
    sudo systemctl status nginx
    ```

    ### Issue 3: Database Connection Error
    ```bash
    # Check database container
    docker logs clientpulse_db

    # Verify DATABASE_URL in .env
    # Ensure db service is healthy
    docker-compose ps
    ```

    ### Issue 4: GitHub Actions Fails
    ```bash
    # Verify all secrets are set correctly
    # Check workflow logs in GitHub Actions tab
    # Ensure ECR repository exists
    # Verify EC2 is accessible via SSH
    ```

    ---

    ## 📚 Additional Resources

    - **Project Repository:** Your GitHub repo URL
    - **API Documentation:** http://<EC2-IP>/docs
    - **Postman Collection:** Included in repo
    - **AWS Console:** https://console.aws.amazon.com
    - **FastAPI Docs:** https://fastapi.tiangolo.com

    ---

    **🎉 Assignment Complete! Good Luck! 🚀**
