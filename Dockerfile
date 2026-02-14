FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY ./app ./app

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    sqlalchemy==2.0.25 \
    pymysql==1.1.0 \
    pydantic==2.5.3 \
    pydantic-settings==2.1.0 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    bcrypt==4.1.2 \
    boto3==1.34.34 \
    python-multipart==0.0.6 \
    python-dotenv==1.0.0\
    email-validator

# Expose port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
