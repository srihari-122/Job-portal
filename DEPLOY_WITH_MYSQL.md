# 🐬 Deploy Job Portal with MySQL on Render

## 🎯 Your Complete MySQL Deployment Guide

Since you're using MySQL, here are your **best FREE options**:

---

## ✅ **RECOMMENDED: PlanetScale MySQL (100% FREE)**

### Why PlanetScale?
- ✅ **Completely FREE** forever
- ✅ **10 GB storage** (generous!)
- ✅ Built-in branching (like Git for databases)
- ✅ No credit card required
- ✅ SSL/TLS included
- ✅ Global edge network
- ✅ Web-based SQL console

---

## 🚀 Complete Deployment Steps

### **PART 1: Setup PlanetScale MySQL (5 minutes)**

#### 1. Create PlanetScale Account
```
🔗 Visit: https://app.planetscale.com/
✅ Sign up with GitHub (fastest)
```

#### 2. Create Your Database
```
1. Click "Create a database"
2. Database name: job-portal-db
3. Region: AWS us-east-1 (or closest to you)
4. Click "Create database"
5. Wait ~30 seconds for provisioning
```

#### 3. Get Connection Password
```
1. Click on "job-portal-db"
2. Click "Connect" button
3. Create a password:
   - Name: render-connection
   - Click "Create password"
4. Select "General" format
5. Copy the connection details:
   - Host: aws.connect.psdb.cloud
   - Username: xxxxxxxxxxxxx
   - Password: pscale_pw_xxxxxxxxxxxxx
```

#### 4. Build Connection String
```
Format for Render:
mysql+pymysql://USERNAME:PASSWORD@HOST/DATABASE?ssl=true

Example:
mysql+pymysql://abcd1234:pscale_pw_xyz789@aws.connect.psdb.cloud/job_portal?ssl=true

⚠️ Replace:
- USERNAME with your username from PlanetScale
- PASSWORD with pscale_pw_xxxxx from PlanetScale
- HOST with the hostname (aws.connect.psdb.cloud)
```

---

### **PART 2: Push Code to GitHub (2 minutes)**

```bash
# Ensure all files are committed
git status

# Add all files
git add .

# Commit changes
git commit -m "Ready for Render deployment with MySQL"

# Push to GitHub
git push origin main
```

---

### **PART 3: Deploy on Render (5 minutes)**

#### 1. Go to Render Dashboard
```
🔗 Visit: https://dashboard.render.com
✅ Sign in or create account
```

#### 2. Create New Web Service
```
1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect a repository"
4. Authorize GitHub access
5. Select your "JOB" repository
6. Click "Connect"
```

#### 3. Configure Your Service
```
Basic Settings:
- Name: job-portal
- Region: Oregon (US West) or closest to you
- Branch: main
- Root Directory: (leave empty)
- Runtime: Python 3

Build Settings:
- Build Command: 
  pip install -r requirements.txt && mkdir -p uploads static/css static/js templates

- Start Command:
  uvicorn main:app --host 0.0.0.0 --port $PORT

Plan:
- Select "Free" plan
```

#### 4. Add Environment Variables (CRITICAL!)
```
Click "Advanced" → "Add Environment Variable"

Add each of these:

1. DATABASE_URL
   Value: mysql+pymysql://user:pass@host.psdb.cloud/job_portal?ssl=true
   (Your PlanetScale connection string from Part 1, Step 4)

2. SECRET_KEY
   Value: (Click "Generate" button)
   
3. DEBUG
   Value: false

4. DATABASE_NAME
   Value: job_portal

5. PYTHON_VERSION
   Value: 3.11

6. ACCESS_TOKEN_EXPIRE_MINUTES
   Value: 1440
```

#### 5. Create Web Service
```
1. Click "Create Web Service" button
2. Wait for deployment (5-10 minutes)
3. Watch the logs for "Application startup complete"
```

---

### **PART 4: Setup Database Tables (3 minutes)**

#### Option A: Using PlanetScale Console (Easiest)

```
1. Go to PlanetScale Dashboard
2. Click on your database
3. Click "Console" tab
4. Paste and run this SQL:
```

```sql
-- Create Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'candidate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Create Jobs Table
CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    salary VARCHAR(100),
    requirements TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Create Applications Table
CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    user_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'applied',
    resume_path VARCHAR(500),
    ai_score INT,
    ai_suggestion VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_application (job_id, user_id)
);

-- Create default admin user (password: Admin@123)
INSERT INTO users (email, password_hash, name, role) VALUES 
('admin@jobportal.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ND.LQ3NlZzHO', 'Admin User', 'admin');
```

```
5. Click "Execute" or "Run"
6. Verify tables created successfully
```

---

## ✅ **PART 5: Test Your Deployment**

### 1. Open Your App
```
Your URL: https://job-portal-xxxx.onrender.com
(Found in Render Dashboard under your service)
```

### 2. Test These Features:
```
✅ Homepage loads
✅ Register new user
✅ Login with registered user
✅ Login as admin:
   - Email: admin@jobportal.com
   - Password: Admin@123
✅ Admin can post jobs
✅ Candidate can view jobs
✅ Candidate can apply to jobs
✅ Upload resume works
✅ AI analysis works
```

### 3. Monitor Logs
```
Render Dashboard → Your Service → Logs

Look for:
✅ "Application startup complete"
✅ "Uvicorn running on http://0.0.0.0:XXXX"
❌ No database connection errors
❌ No 500 errors
```

---

## 🔧 Troubleshooting

### Issue: "Can't connect to database"

**Check:**
1. DATABASE_URL format is correct:
   ```
   mysql+pymysql://user:pass@host/database?ssl=true
   ```
2. Username and password are correct
3. Database name matches (job_portal)
4. PlanetScale database is "Ready" status

**Fix:**
```bash
# Test connection locally
export DATABASE_URL="your-connection-string"
python test_mysql.py
```

---

### Issue: "Table doesn't exist"

**Fix:**
Run the SQL schema from Part 4 in PlanetScale Console

---

### Issue: "SSL connection required"

**Fix:**
Add `?ssl=true` to connection string:
```
mysql+pymysql://user:pass@host/db?ssl=true
```

---

### Issue: "Access denied for user"

**Fix:**
1. Verify username and password from PlanetScale
2. Create new password in PlanetScale if needed
3. Update DATABASE_URL in Render

---

## 📊 Database Management

### View Your Data
```
PlanetScale Dashboard → Your Database → Console
Run SQL: SELECT * FROM users;
```

### Backup Your Database
```
PlanetScale automatically backs up your data
You can also export:
PlanetScale Dashboard → Backups → Download
```

### Monitor Performance
```
PlanetScale Dashboard → Insights
- Query performance
- Connection stats
- Storage usage
```

---

## 🎓 Learning Resources

- **PlanetScale Tutorial:** https://planetscale.com/docs/tutorials/planetscale-quick-start-guide
- **MySQL Documentation:** https://dev.mysql.com/doc/
- **SQLAlchemy Tutorial:** https://docs.sqlalchemy.org/en/14/tutorial/
- **Render Deployment:** https://render.com/docs/deploy-fastapi

---

## 🎉 **YOU'RE ALL SET!**

### Your Setup:
- ✅ MySQL Database: PlanetScale (FREE)
- ✅ Web Hosting: Render (FREE)
- ✅ Total Cost: $0/month
- ✅ Professional UI: ✨
- ✅ AI Features: 🤖

### Deployment Time:
- Database Setup: 5 minutes
- Code Push: 2 minutes
- Render Deploy: 5 minutes
- **Total: ~12 minutes**

---

## 🚀 Deploy Now!

```bash
# Quick command summary:
git add .
git commit -m "Deploy with MySQL"
git push origin main

# Then visit:
https://dashboard.render.com

# Create Web Service → Add DATABASE_URL → Deploy!
```

---

## 📞 Need Help?

1. **Check Render Logs** - Most issues show here
2. **Verify PlanetScale** - Ensure database is "Ready"
3. **Test Connection** - Run test_mysql.py locally
4. **Read Docs** - See MYSQL_SETUP_COMPLETE.md

---

**Your Job Portal is ready to go live with MySQL! 🎊**

**Default Admin Login:**
- Email: admin@jobportal.com
- Password: Admin@123

**Remember to change this after first login!**

---

**Happy Deploying! 🚀✨**




