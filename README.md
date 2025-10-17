# Job Portal - AI-Powered Job Search Platform

A comprehensive job portal application that connects job seekers with recruiters using advanced AI analysis and machine learning features.

## 🚀 Features

### Core Functionality
- **Dual Dashboard System**: Separate dashboards for candidates and admins
- **Real Email Validation**: Domain verification for authentic user registration
- **JWT Authentication**: Secure token-based authentication system
- **Resume Processing**: AI-powered PDF resume content extraction
- **Job Management**: Complete CRUD operations for job postings

### AI & ML Features
- **Skill Gap Analysis**: Compare candidate skills with job requirements
- **Salary Projection**: AI-powered salary predictions based on profile and location
- **Career Growth Analysis**: Personalized career advancement recommendations
- **Location Growth Analysis**: Market insights for different geographic locations
- **Resume Content Extraction**: Automatic extraction of skills, experience, and qualifications
- **Career Path Recommendations**: Tailored guidance for freshers and experienced professionals

### User Experience
- **Responsive Design**: Modern UI/UX with Tailwind CSS
- **Real-time Notifications**: Toast notifications for user feedback
- **File Upload**: Drag-and-drop resume upload functionality
- **Search & Filter**: Advanced job search capabilities
- **Application Tracking**: Complete application management system

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MySQL**: Relational database for data storage
- **JWT**: Secure authentication tokens
- **PyPDF2**: PDF processing for resume extraction
- **spaCy**: Natural language processing
- **scikit-learn**: Machine learning algorithms
- **pandas/numpy**: Data analysis and manipulation

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive user interface
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library

### AI/ML Libraries
- **spaCy**: NLP for text processing
- **scikit-learn**: ML algorithms for analysis
- **TF-IDF Vectorization**: Text similarity analysis
- **Cosine Similarity**: Skill matching algorithms

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+
- pip (Python package manager)
- Git (for version control)

## 🚀 Quick Start

### 1. Navigate to Project Directory
```bash
cd job
```

### 2. Run Setup Script
```bash
python setup.py
```

The setup script will:
- Install all Python dependencies
- Create necessary directories
- Set up MySQL database and tables
- Download required ML models
- Create environment configuration file

### 3. Configure Environment
Edit the `.env` file with your configuration:
```env
SECRET_KEY=your-secret-key-change-in-production
DB_HOST=localhost
DB_NAME=job_portal
DB_USER=root
DB_PASSWORD=your-mysql-password
```

### 4. Setup Database Structure (Optional)
```bash
python sample_data.py
```

### 5. Start the Application
```bash
python start.py
```

### 6. Access the Application
Open your browser and navigate to: `http://localhost:8000`

### 7. Register Your Own Account
- **No sample data provided** - you must register with your own real email address
- **Only real, authorized email domains are allowed** (Gmail, Yahoo, Outlook, corporate emails, etc.)
- **Create your own admin or candidate account** during registration

## 📁 Project Structure

```
job/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── setup.py               # Setup and installation script
├── start.py               # Application startup script
├── test_app.py            # Comprehensive testing suite
├── sample_data.py         # Sample data generator
├── config.py              # Configuration management
├── README.md              # Project documentation
├── DEPLOYMENT_GUIDE.md    # Deployment instructions
├── PROJECT_SUMMARY.md     # Project overview
├── .env                   # Environment configuration
├── templates/             # HTML templates
│   └── index.html        # Main application template
├── static/               # Static files
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── app.js       # Frontend JavaScript
└── uploads/              # File upload directory
```

## 🔧 Manual Installation

If you prefer manual installation:

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 3. Setup MySQL Database
```sql
CREATE DATABASE job_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Configure Database Connection
Update the `DB_CONFIG` in `main.py` with your MySQL credentials.

## 🎯 Usage Guide

### For Job Seekers (Candidates)

1. **Register/Login**: Create account with valid email domain
2. **Upload Resume**: Upload PDF resume for AI analysis
3. **Browse Jobs**: Search and filter available positions
4. **Apply for Jobs**: Submit applications with cover letters
5. **View AI Analysis**: Get insights on skill gaps, salary projections, and career growth
6. **Track Applications**: Monitor application status and responses

### For Recruiters (Admins)

1. **Register/Login**: Create admin account
2. **Post Jobs**: Create detailed job listings
3. **Manage Applications**: Review candidate applications
4. **View Analytics**: Monitor hiring metrics and trends
5. **AI Insights**: Access ML analysis of candidate profiles

## 🤖 AI Features Explained

### Skill Gap Analysis
- Compares candidate skills with job requirements
- Calculates match percentage
- Identifies missing skills
- Provides learning recommendations

### Salary Projection
- Analyzes candidate profile and experience
- Considers location and market factors
- Provides realistic salary expectations
- Updates based on skill development

### Career Growth Analysis
- Assesses current career level
- Suggests next steps for advancement
- Provides timeline estimates
- Recommends skill development areas

### Location Growth Analysis
- Analyzes job market trends by location
- Compares cost of living and opportunities
- Matches candidate skills with local demand
- Provides relocation recommendations

## 🔒 Security Features

- **Strict Email Validation**: Only legitimate business, educational, and government domains allowed
  - Major email providers: Gmail, Yahoo, Outlook, etc.
  - Educational domains: .edu, .ac.uk, .edu.au, etc.
  - Government domains: .gov, .gov.uk, .gov.au, etc.
  - Major corporations: Microsoft, Google, Apple, Amazon, etc.
  - Indian companies: TCS, Infosys, Wipro, HCL, etc.
  - DNS MX record verification for other domains
- **JWT Authentication**: Secure token-based sessions
- **Password Hashing**: SHA-256 encryption for passwords
- **Input Validation**: Comprehensive form validation
- **File Upload Security**: PDF-only uploads with validation
- **SQL Injection Prevention**: Parameterized queries

## 📊 Database Schema

### Users Table
- User authentication and profile data
- Role-based access control
- JSON profile data for ML analysis

### Jobs Table
- Job postings and requirements
- Company and location information
- Salary ranges and job types

### Applications Table
- Job application records
- Resume content and ML analysis
- Application status tracking

### ML Analysis Table
- Stored AI analysis results
- Historical analysis data
- Performance metrics

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
1. Update `.env` with production settings
2. Use a production WSGI server (Gunicorn)
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates
5. Configure MySQL for production

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## 🧪 Testing

### Manual Testing
1. Register with valid email domains
2. Upload PDF resumes
3. Create job postings
4. Submit applications
5. Verify AI analysis accuracy

### API Testing
Use tools like Postman or curl to test API endpoints:
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password","full_name":"Test User","role":"candidate"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints

## 🔮 Future Enhancements

- **Email Notifications**: Automated email alerts
- **Advanced ML Models**: Enhanced AI analysis
- **Mobile App**: React Native mobile application
- **Video Interviews**: Integrated video calling
- **Social Login**: OAuth integration
- **Advanced Analytics**: Detailed reporting dashboard
- **Multi-language Support**: Internationalization
- **API Rate Limiting**: Enhanced security
- **Caching**: Redis integration for performance
- **Microservices**: Scalable architecture

## 📈 Performance Optimization

- **Database Indexing**: Optimized query performance
- **Caching Strategy**: Reduced response times
- **File Compression**: Optimized asset delivery
- **CDN Integration**: Global content delivery
- **Load Balancing**: Scalable architecture

---

**Built with ❤️ using FastAPI, MySQL, and AI/ML technologies**

