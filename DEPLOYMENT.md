# Job Portal Deployment Guide

## 🚀 Deployment Options

### Option 1: Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Configure Environment Variables**
   - Go to Vercel Dashboard
   - Select your project
   - Go to Settings > Environment Variables
   - Add the following variables:
     - `EMAIL_USERNAME`: Your Gmail address
     - `EMAIL_PASSWORD`: Your Gmail app password
     - `MONGODB_URL`: Your MongoDB connection string
     - `SECRET_KEY`: Your JWT secret key

### Option 2: Render Deployment

1. **Connect GitHub Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" > "Web Service"
   - Connect your GitHub repository

2. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - `EMAIL_USERNAME`: Your Gmail address
   - `EMAIL_PASSWORD`: Your Gmail app password
   - `MONGODB_URL`: Your MongoDB connection string
   - `SECRET_KEY`: Your JWT secret key

### Option 3: Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

3. **Start the Application**
   ```bash
   python main.py
   ```

## 📧 Email Configuration

### Gmail Setup

1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Enable 2-Factor Authentication

2. **Generate App Password**
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Generate a new app password for "Mail"
   - Use this password in `EMAIL_PASSWORD`

3. **Update Configuration**
   ```python
   EMAIL_USERNAME = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-16-character-app-password"
   ```

## 🗄️ Database Configuration

### MongoDB Atlas (Recommended)

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Create a free cluster

2. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database password

3. **Update Configuration**
   ```python
   MONGODB_URL = "mongodb+srv://username:password@cluster.mongodb.net/jobportal"
   ```

### Local MongoDB

1. **Install MongoDB**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install mongodb

   # macOS
   brew install mongodb

   # Windows
   # Download from https://www.mongodb.com/try/download/community
   ```

2. **Start MongoDB**
   ```bash
   sudo systemctl start mongodb
   ```

3. **Update Configuration**
   ```python
   MONGODB_URL = "mongodb://localhost:27017"
   ```

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# Email Configuration
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=jobportal

# JWT Secret Key
SECRET_KEY=your-secret-key-here

# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## 🚀 Production Checklist

- [ ] Set up MongoDB database
- [ ] Configure email service
- [ ] Set secure JWT secret key
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure backup strategy
- [ ] Test all features
- [ ] Set up error logging

## 📱 Features Verification

### Candidate Features
- [ ] User registration and login
- [ ] Resume upload and processing
- [ ] Job search and filtering
- [ ] Job application system
- [ ] Application status tracking
- [ ] AI-powered resume analysis

### Admin Features
- [ ] Job posting and management
- [ ] User management
- [ ] Application management
- [ ] Analytics dashboard
- [ ] Email notifications

## 🐛 Troubleshooting

### Common Issues

1. **Email Not Sending**
   - Check Gmail app password
   - Verify SMTP settings
   - Check firewall settings

2. **Database Connection Failed**
   - Verify MongoDB URL
   - Check network connectivity
   - Verify credentials

3. **File Upload Issues**
   - Check file size limits
   - Verify upload directory permissions
   - Check file type validation

### Support

For issues and questions:
- Check the logs for error messages
- Verify environment variables
- Test locally before deploying
- Check deployment platform documentation
