  # ClientPulse - Manual Setup & Testing Guide

## 📦 Step 1: Install Poetry (if not already installed)

```bash
cd ~/clientpulse

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
poetry --version
```

## 🔧 Step 2: Install Project Dependencies

```bash
# Install all dependencies from pyproject.toml
poetry install

# Activate virtual environment
poetry shell
```

## 🗄️ Step 3: Set Up MySQL Database

```bash
# Start MySQL service
sudo service mysql start

# Create database
mysql -u root -p
```

In MySQL prompt:
```sql
CREATE DATABASE clientpulse;
SHOW DATABASES;
EXIT;
```

## ⚙️ Step 4: Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env
```

Update these values in `.env`:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/clientpulse
JWT_SECRET_KEY=change-this-to-a-random-secret-key
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=clientpulse-screenshots
```

## 🔄 Step 5: Initialize Database Migrations (Optional)

```bash
# Initialize Alembic (if you want to use migrations)
poetry run alembic init alembic

# OR just let SQLAlchemy create tables automatically
# (Tables will be created when you run the app)
```

## 🚀 Step 6: Run the Application

```bash
# Method 1: Using uvicorn directly
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Method 2: Using python
poetry run python -m uvicorn app.main:app --reload

# Method 3: Direct execution
cd ~/clientpulse
poetry shell
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 Step 7: Access the API

Open your browser:
- **Swagger Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000/

## 🧪 Step 8: Test APIs with curl

### Test 1: Submit Feedback (without screenshot)
```bash
curl -X POST "http://localhost:8000/api/feedback/" \
  -F "name=Test User" \
  -F "email=test@example.com" \
  -F "rating=5" \
  -F "description=This is a test feedback"
```

### Test 2: Register Admin
```bash
curl -X POST "http://localhost:8000/api/admin/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@clientpulse.com",
    "password": "SecurePassword123!"
  }'
```

### Test 3: Admin Login (Get JWT Token)
```bash
curl -X POST "http://localhost:8000/api/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SecurePassword123!"
  }'
```

Save the `access_token` from the response!

### Test 4: Get Analytics (with JWT)
```bash
# Replace YOUR_TOKEN with the actual token
curl -X GET "http://localhost:8000/api/analytics/reports" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test 5: Download CSV Report
```bash
curl -X GET "http://localhost:8000/api/analytics/download?format=csv" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output feedbacks.csv
```

## 📬 Step 9: Import Postman Collection

1. Open Postman
2. Click **Import**
3. Select `ClientPulse_API.postman_collection.json`
4. Update environment variable `base_url` to `http://localhost:8000`
5. Run "Admin Login" to auto-save token
6. Test all endpoints!

## 🐳 Step 10: Run with Docker (Optional)

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## ✅ Verification Checklist

- [ ] Poetry installed and virtual environment activated
- [ ] MySQL database created
- [ ] .env file configured
- [ ] Application starts without errors
- [ ] Swagger docs accessible at /docs
- [ ] Can submit feedback successfully
- [ ] Can register admin user
- [ ] Can login and get JWT token
- [ ] Can access analytics with JWT
- [ ] Postman collection works

## 🔧 Troubleshooting

### Issue: "poetry: command not found"
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### Issue: "ModuleNotFoundError"
```bash
poetry install
poetry shell
```

### Issue: MySQL connection error
```bash
# Check MySQL is running
sudo service mysql status

# Verify database exists
mysql -u root -p -e "SHOW DATABASES;"

# Check DATABASE_URL in .env
```

### Issue: S3 upload fails
- S3 will fail gracefully if not configured
- Feedback will still be saved without screenshot
- Configure AWS credentials in .env to enable S3

## 📊 Next Steps

1. **Test all APIs** using Swagger UI or Postman
2. **Add more test data** via feedback submissions
3. **Set up AWS S3** bucket for screenshot uploads
4. **Configure CI/CD** with GitHub Actions
5. **Deploy to EC2** when ready

## 🎯 Production Deployment

When ready for deployment:
1. Set up AWS ECR repository
2. Configure GitHub Secrets
3. Push to main branch → Auto deploy via GitHub Actions
4. Configure domain and HTTPS with Let's Encrypt

---

Happy coding! 🚀
