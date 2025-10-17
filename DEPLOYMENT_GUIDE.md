# Job Portal - Deployment Guide

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+
- pip (Python package manager)

### 1. Setup and Installation

```bash
# Clone or download the project
cd job-portal

# Run the automated setup
python setup.py
```

The setup script will:
- ✅ Install all Python dependencies
- ✅ Create necessary directories
- ✅ Set up MySQL database and tables
- ✅ Download required ML models
- ✅ Create environment configuration

### 2. Configure Environment

Edit the `.env` file with your settings:
```env
SECRET_KEY=your-secret-key-change-in-production
DB_HOST=localhost
DB_NAME=job_portal
DB_USER=root
DB_PASSWORD=your-mysql-password
```

### 3. Add Sample Data (Optional)

```bash
python sample_data.py
```

This creates:
- Sample admin user: `admin@techcorp.com` / `admin123`
- Sample candidates with profiles
- Sample job postings
- Sample applications

### 4. Start the Application

```bash
# Option 1: Use the startup script
python start.py

# Option 2: Direct FastAPI
python main.py

# Option 3: Uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the Application

Open your browser: `http://localhost:8000`

## 🧪 Testing the Application

```bash
# Run automated tests
python test_app.py
```

## 📋 Manual Testing Checklist

### Authentication
- [ ] Register with valid email domain
- [ ] Login with correct credentials
- [ ] JWT token authentication works
- [ ] Logout functionality

### Candidate Features
- [ ] Upload PDF resume
- [ ] Resume content extraction works
- [ ] Browse job listings
- [ ] Apply for jobs
- [ ] View application status
- [ ] AI analysis results display

### Admin Features
- [ ] Post new job listings
- [ ] Manage job postings
- [ ] View candidate applications
- [ ] Update application status
- [ ] View analytics dashboard

### AI/ML Features
- [ ] Skill gap analysis accuracy
- [ ] Salary projection calculations
- [ ] Career growth recommendations
- [ ] Location analysis insights
- [ ] Resume content extraction

## 🔧 Configuration Options

### Database Configuration
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'job_portal',
    'user': 'root',
    'password': 'your_password',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

### ML Model Settings
```python
SPACY_MODEL = 'en_core_web_sm'
SKILL_KEYWORDS = ['python', 'javascript', 'react', ...]
BASE_SALARIES = {'software engineer': 85000, ...}
```

### File Upload Settings
```python
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'pdf'}
```

## 🌐 Production Deployment

### 1. Environment Setup
```bash
# Set production environment
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DB_PASSWORD=your-production-db-password
```

### 2. Database Setup
```sql
-- Create production database
CREATE DATABASE job_portal_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create dedicated user
CREATE USER 'jobportal_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON job_portal_prod.* TO 'jobportal_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Server Configuration
```bash
# Install production server
pip install gunicorn

# Start with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔒 Security Considerations

### 1. Environment Variables
- Never commit `.env` files to version control
- Use strong, unique secret keys
- Rotate secrets regularly

### 2. Database Security
- Use dedicated database users
- Enable SSL connections
- Regular backups
- Monitor access logs

### 3. Application Security
- Enable HTTPS in production
- Implement rate limiting
- Validate all inputs
- Sanitize file uploads

### 4. ML Model Security
- Validate resume content
- Limit file sizes
- Scan for malicious content
- Monitor model performance

## 📊 Monitoring and Maintenance

### 1. Application Monitoring
```bash
# Check application logs
tail -f app.log

# Monitor database connections
mysqladmin processlist

# Check disk usage
df -h
```

### 2. Performance Optimization
- Enable database indexing
- Implement caching (Redis)
- Optimize ML model loading
- Use CDN for static files

### 3. Regular Maintenance
- Update dependencies monthly
- Backup database weekly
- Monitor disk space
- Review error logs

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check MySQL status
sudo systemctl status mysql

# Test connection
mysql -u root -p -e "SHOW DATABASES;"
```

#### ML Model Not Found
```bash
# Download spaCy model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')"
```

#### File Upload Issues
```bash
# Check upload directory permissions
ls -la uploads/
chmod 755 uploads/
```

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Error Logs
Check these locations for error information:
- Application logs: `app.log`
- System logs: `/var/log/syslog`
- Nginx logs: `/var/log/nginx/error.log`
- MySQL logs: `/var/log/mysql/error.log`

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Multiple application instances
- Database read replicas
- Session storage (Redis)

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching layers
- Use faster storage (SSD)

### Microservices Architecture
- Separate ML service
- Dedicated file service
- Independent notification service
- API gateway

## 🔄 Backup and Recovery

### Database Backup
```bash
# Create backup
mysqldump -u root -p job_portal > backup_$(date +%Y%m%d).sql

# Restore backup
mysql -u root -p job_portal < backup_20240101.sql
```

### File Backup
```bash
# Backup uploads directory
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/

# Backup application files
tar -czf app_backup_$(date +%Y%m%d).tar.gz --exclude=__pycache__ --exclude=*.pyc .
```

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Test with sample data
4. Verify all dependencies are installed

## 🎯 Next Steps

After successful deployment:
1. Configure monitoring alerts
2. Set up automated backups
3. Implement CI/CD pipeline
4. Add performance monitoring
5. Plan for scaling

---

**Your Job Portal is now ready for production use! 🎉**