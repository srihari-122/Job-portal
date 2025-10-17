# 🐬 Complete MySQL Setup Guide for Render Deployment

## 🎯 Overview

Your Job Portal supports **MySQL database**. Here are all your options:

---

## 📊 MySQL Options Comparison

| Provider | Free Tier | Storage | Setup Time | Recommended |
|----------|-----------|---------|------------|-------------|
| **PostgreSQL (Render)** | ✅ Yes | 1 GB | 1 min | ⭐⭐⭐⭐⭐ |
| **PlanetScale** | ✅ Yes | 10 GB | 3 min | ⭐⭐⭐⭐ |
| **Railway** | ✅ Limited | 1 GB | 3 min | ⭐⭐⭐ |
| **Render MySQL** | ❌ No | Custom | 1 min | ⭐⭐ (Paid) |
| **AWS RDS MySQL** | ⚠️ Limited | 20 GB | 10 min | ⭐⭐⭐ |

---

## 🆓 Option 1: PostgreSQL on Render (EASIEST & FREE)

### Why Choose This?
- ✅ **Completely FREE**
- ✅ **Zero configuration** needed
- ✅ Automatic setup via `render.yaml`
- ✅ Managed by Render
- ✅ Automatic backups
- ✅ No external service needed

### How to Deploy:
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy with PostgreSQL"
git push origin main

# 2. Go to Render
https://dashboard.render.com

# 3. New+ → Blueprint → Select repo → Apply

# 4. Done! Database is auto-created!
```

**Connection String Format:**
```
postgresql://user:password@host.render.com:5432/database
```

---

## 🐬 Option 2: PlanetScale MySQL (FREE)

### Step-by-Step Setup

#### 1. Create PlanetScale Account
```
Visit: https://planetscale.com
Sign up with GitHub (easiest)
```

#### 2. Create Database
```
1. Click "New database"
2. Name: job-portal-db
3. Region: us-east (or closest to your Render region)
4. Click "Create database"
```

#### 3. Get Connection String
```
1. Click on your database
2. Click "Connect"
3. Select "Connect with: General"
4. Copy the connection string:
   
   mysql://user:pscale_pw_xxxxx@host.psdb.cloud/job_portal?sslaccept=strict
```

#### 4. Update Connection String Format
```
Change from:
mysql://user:password@host/database

To (for SQLAlchemy):
mysql+pymysql://user:password@host/database?ssl=true
```

#### 5. Deploy to Render
```
1. Go to https://dashboard.render.com
2. New+ → Web Service
3. Connect GitHub repo
4. Build: pip install -r requirements.txt && mkdir -p uploads
5. Start: uvicorn main:app --host 0.0.0.0 --port $PORT
6. Add environment variable:
   - DATABASE_URL: [Your PlanetScale connection string]
7. Create Web Service
```

---

## 🚂 Option 3: Railway MySQL (FREE with Limits)

### Step-by-Step Setup

#### 1. Create Railway Account
```
Visit: https://railway.app
Sign up with GitHub
```

#### 2. Create MySQL Database
```
1. New Project
2. Add "MySQL" from template
3. Database will be provisioned automatically
```

#### 3. Get Connection String
```
1. Click on MySQL service
2. Go to "Variables" tab
3. Copy these values:
   - MYSQL_HOST
   - MYSQL_USER
   - MYSQL_PASSWORD
   - MYSQL_DATABASE
   - MYSQL_PORT
```

#### 4. Build Connection String
```
Format:
mysql+pymysql://MYSQL_USER:MYSQL_PASSWORD@MYSQL_HOST:MYSQL_PORT/MYSQL_DATABASE

Example:
mysql+pymysql://root:password123@containers.railway.app:3306/railway
```

#### 5. Deploy to Render
```
Same as PlanetScale (Option 2, Step 5)
Use your Railway connection string
```

---

## 💰 Option 4: Render MySQL (PAID - $7/month)

### Update render.yaml
```yaml
databases:
  - name: job-portal-db
    databaseName: job_portal
    user: jobportal_user
    plan: starter  # $7/month
```

### Deploy
```
Use Blueprint method - database created automatically
```

---

## 🔧 MySQL Connection String Formats

### Standard MySQL
```
mysql+pymysql://username:password@hostname:3306/database_name
```

### MySQL with SSL
```
mysql+pymysql://username:password@hostname:3306/database_name?ssl=true
```

### PlanetScale Format
```
mysql+pymysql://username:pscale_pw_xxxxx@hostname.psdb.cloud/database?ssl={"rejectUnauthorized":true}
```

### Railway Format
```
mysql+pymysql://root:password@containers.railway.app:3306/railway
```

---

## 🗄️ Database Schema Setup

After deployment, you need to create tables:

### Option A: Using SQLAlchemy (Recommended)

Add to your `main.py`:
```python
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255))
    role = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    description = Column(Text)
    location = Column(String(255))
    salary = Column(String(100))
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(50), default='applied')
    resume_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)
```

### Option B: Manual SQL

Connect to your database and run:
```sql
-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'candidate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    salary VARCHAR(100),
    requirements TEXT,
    benefits TEXT,
    job_type VARCHAR(50),
    experience_level VARCHAR(50),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_created_by (created_by),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Applications Table
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    user_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'applied',
    resume_path VARCHAR(500),
    ai_score INT,
    ai_suggestion VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_job_user (job_id, user_id),
    INDEX idx_status (status),
    UNIQUE KEY unique_application (job_id, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Resumes Table (Optional)
CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_path VARCHAR(500),
    extracted_data JSON,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create default admin user (password: admin123)
INSERT INTO users (email, password_hash, name, role) VALUES 
('admin@jobportal.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ND.LQ3NlZzHO', 'Admin User', 'admin')
ON DUPLICATE KEY UPDATE email=email;
```

---

## 🧪 Testing Database Connection

### Test Locally
```python
# test_mysql.py
from sqlalchemy import create_engine, text
import os

# Your connection string
DATABASE_URL = "mysql+pymysql://user:pass@host:3306/database"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ MySQL connection successful!")
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
```

```bash
python test_mysql.py
```

---

## 🔐 MySQL Best Practices

### 1. Connection Pooling
```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600    # Recycle connections after 1 hour
)
```

### 2. SSL Configuration
```python
# For production
DATABASE_URL = "mysql+pymysql://user:pass@host/db?ssl=true"
```

### 3. Character Set
```python
# Use UTF-8 for international characters
DATABASE_URL = "mysql+pymysql://user:pass@host/db?charset=utf8mb4"
```

---

## 📊 Database Management Tools

### PlanetScale
- Web console included
- CLI tool available
- Branch-based development

### Railway
- Built-in database viewer
- Direct SQL execution
- Metrics dashboard

### PostgreSQL (Render)
- Built-in dashboard
- Connection pooling
- Automatic backups

---

## 🚨 Common MySQL Issues & Solutions

### Issue: "Access denied"
```sql
-- Grant privileges
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'%';
FLUSH PRIVILEGES;
```

### Issue: "SSL connection error"
```python
# Add SSL parameter
DATABASE_URL = "mysql+pymysql://user:pass@host/db?ssl=true"
```

### Issue: "Too many connections"
```python
# Reduce pool size
engine = create_engine(DATABASE_URL, pool_size=3, max_overflow=5)
```

### Issue: "Lost connection to MySQL server"
```python
# Enable connection pre-ping
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
```

---

## 🔄 Migration from MongoDB to MySQL

If your code currently uses MongoDB, here's how to convert:

### 1. Install MySQL Driver
```bash
pip install pymysql sqlalchemy
```

### 2. Replace Database Code
```python
# OLD (MongoDB)
from pymongo import MongoClient
client = MongoClient(DATABASE_URL)
db = client.job_portal
users = db.users.find_one({"email": email})

# NEW (MySQL with SQLAlchemy)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
user = session.query(User).filter_by(email=email).first()
```

### 3. Update Queries
```python
# MongoDB style
db.users.insert_one(user_dict)
db.users.find({"role": "admin"})
db.users.update_one({"_id": id}, {"$set": data})

# MySQL/SQLAlchemy style
session.add(user_object)
session.query(User).filter_by(role="admin").all()
session.query(User).filter_by(id=id).update(data)
session.commit()
```

---

## 📝 Quick Deploy Commands

### With PostgreSQL (Recommended)
```bash
git add .
git commit -m "Deploy with PostgreSQL on Render"
git push origin main
# Then: Render Dashboard → New+ → Blueprint
```

### With PlanetScale MySQL
```bash
# 1. Create database on PlanetScale
# 2. Get connection string
git add .
git commit -m "Deploy with PlanetScale MySQL"
git push origin main
# 3. Deploy: Render Dashboard → New+ → Web Service
# 4. Add DATABASE_URL environment variable
```

---

## 🎯 Recommended Setup

For **easiest deployment** with **zero cost**:

1. ✅ Use **PostgreSQL on Render** (automatic, free, managed)
2. Deploy via **Blueprint** method
3. Let Render handle everything!

For **specific MySQL requirement**:

1. Use **PlanetScale** (10GB free, easy setup)
2. Deploy via **Web Service** method
3. Add DATABASE_URL manually

---

## 📞 Support Resources

- **PlanetScale Docs:** https://planetscale.com/docs
- **Railway Docs:** https://docs.railway.app/databases/mysql
- **Render PostgreSQL:** https://render.com/docs/databases
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/

---

## ✅ Final Checklist

Before deploying with MySQL:

- [ ] Database provider chosen (PlanetScale/Railway/PostgreSQL)
- [ ] Database created
- [ ] Connection string obtained
- [ ] Connection string tested locally
- [ ] `requirements.txt` includes `pymysql` and `sqlalchemy`
- [ ] Database tables created (schema setup)
- [ ] Code updated to use SQLAlchemy (if needed)
- [ ] Environment variables ready

---

## 🎉 Ready to Deploy!

**Recommended Path:**
1. Use **PostgreSQL on Render** (easiest, free, automatic)
2. Deploy via Blueprint
3. Live in 10 minutes!

**Alternative Path:**
1. Use **PlanetScale MySQL** (if MySQL required)
2. Deploy via Web Service
3. Add DATABASE_URL manually
4. Live in 15 minutes!

---

**Choose your path and deploy! 🚀**

For quick start: See `QUICKSTART_RENDER.md`
For detailed guide: See `MYSQL_DEPLOYMENT_GUIDE.md`

Good luck! 🎊✨




