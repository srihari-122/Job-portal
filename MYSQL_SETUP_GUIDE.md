# 🔧 MySQL Database Setup Guide

## Quick Fix for MySQL Connection Issue

The error you're seeing is because MySQL requires a password, but the application is trying to connect without one.

## Solution Steps:

### 1. Run the Database Setup Script
```bash
python database_setup.py
```

This script will:
- Ask for your MySQL credentials
- Test the connection
- Create the database and tables
- Generate a `.env` file with your configuration

### 2. Alternative: Manual Setup

If you prefer to set up manually:

#### Step 1: Create .env file
Create a `.env` file in the `job` folder with your MySQL credentials:

```env
SECRET_KEY=your-secret-key-change-in-production
DB_HOST=localhost
DB_PORT=3306
DB_NAME=job_portal
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci
```

#### Step 2: Create Database Manually
Connect to MySQL and run:

```sql
CREATE DATABASE job_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Common MySQL Issues & Solutions

#### Issue 1: "Access denied for user 'root'@'localhost'"
**Solution**: Your MySQL root user has a password. Use the database setup script to configure it properly.

#### Issue 2: MySQL service not running
**Solution**: Start MySQL service:
```bash
# Windows (as Administrator)
net start mysql

# Or through Services
services.msc -> MySQL -> Start
```

#### Issue 3: Forgot MySQL root password
**Solution**: Reset MySQL root password:

1. Stop MySQL service
2. Start MySQL in safe mode:
```bash
mysqld --skip-grant-tables
```
3. Connect and reset password:
```sql
USE mysql;
UPDATE user SET authentication_string=PASSWORD('newpassword') WHERE User='root';
FLUSH PRIVILEGES;
```

### 4. Test Your Setup

After configuration, test the connection:

```bash
python -c "
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'job_portal'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', '3306'))
}

try:
    connection = mysql.connector.connect(**config)
    print('✅ MySQL connection successful!')
    connection.close()
except Exception as e:
    print(f'❌ Connection failed: {e}')
"
```

### 5. Start the Application

Once the database is configured:

```bash
python start.py
```

## Need Help?

If you're still having issues:

1. **Check MySQL Status**: Make sure MySQL service is running
2. **Verify Credentials**: Double-check your MySQL username and password
3. **Check Port**: Ensure MySQL is running on port 3306 (default)
4. **Firewall**: Make sure Windows Firewall isn't blocking MySQL

## Sample .env File

Here's a complete `.env` file template:

```env
# Job Portal Environment Configuration
SECRET_KEY=your-secret-key-change-in-production-12345
DB_HOST=localhost
DB_PORT=3306
DB_NAME=job_portal
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# ML Model Configuration
SPACY_MODEL=en_core_web_sm
```

Replace `your_mysql_password` with your actual MySQL root password.
