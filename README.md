# School_SaaS

A comprehensive Flask-based School SaaS backend providing authentication, student/course/class management, attendance tracking, grade management, and AI integrations (OpenAI). Built for scalability with multi-tenancy support and containerization.

## 🎯 Key Features

- **Authentication** - JWT-based user authentication with role-based access control
- **User Management** - Support for admins, teachers, students, parents, and staff
- **Student Management** - Complete student profiles with enrollment tracking
- **Course Management** - Create and manage courses with class assignments
- **Attendance Tracking** - Mark and track student attendance per class
- **Grade Management** - Track and manage student grades by course and term
- **Multi-tenancy** - Support for multiple school instances on single deployment
- **AI Integration** - Optional OpenAI integration for smart features
- **Async Tasks** - Celery support for background job processing
- **Production Ready** - Docker, Kubernetes, Terraform, and Ansible configurations included

## 📋 Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- Git (optional)
- Docker & Docker Compose (optional, for containerized setup)

## ⚡ Quick Start (Local Development)

### Automated Setup (Recommended)

**PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\setup.ps1
```

**Command Prompt:**
```cmd
setup.bat
```

### Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1      # PowerShell
# OR
venv\Scripts\activate.bat        # Command Prompt

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set Flask app
$env:FLASK_APP = 'app.py'

# 5. Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 6. Run the app
python app.py
```

The API will be available at **http://localhost:5000**

## 📖 For Detailed Local Setup Instructions

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for comprehensive setup guide including:
- Step-by-step installation
- Troubleshooting
- Testing endpoints
- Useful commands

## 🏗️ Project Structure

```
School_SaaS/
├── app.py                          # Flask app entry point
├── config.py                       # Configuration management
├── models.py                       # SQLAlchemy database models
├── routes/                         # Package containing per‑resource blueprints
├── services.py                     # Business logic layer
├── utils.py                        # Utility functions & decorators
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (local)
├── data.db                         # SQLite database (auto-created)
│
├── LOCAL_SETUP.md                  # 👈 Local development guide
├── setup.ps1 & setup.bat           # Automated setup scripts
│
├── Docker/
│   ├── Dockerfile                  # Application container
│   ├── docker-compose.yml          # Local/dev Docker setup
│   └── docker-compose.monitor.yml  # Monitoring stack
│
├── Kubernetes/
│   ├── base/                       # Base k8s resources
│   └── production/                 # Production overlays
│
├── Terraform/                      # Infrastructure as Code (AWS)
└── Ansible/                        # Configuration management
```

## 📝 Environment Variables

The app uses `.env` file for local configuration (already set up for you). Key variables:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret
SQLALCHEMY_DATABASE_URI=sqlite:///data.db

# Optional - leave empty to disable
CELERY_BROKER_URL=
OPENAI_API_KEY=
```

See `.env` file for all available options.

## 🚀 Running the Application

### Development Server
```powershell
python app.py
```

Server will start at `http://localhost:5000`

### With Custom Port
```powershell
python -c "from app import app; app.run(port=8000)"
```

### Using Flask CLI
```powershell
flask run --host=0.0.0.0 --port=5000
```

## 🧪 Testing the API

### Health Check
```powershell
Invoke-WebRequest http://localhost:5000/health
```

### Register User
```powershell
$body = @{
    email = "test@example.com"
    password = "password123"
    first_name = "John"
    last_name = "Doe"
    user_type = 3
} | ConvertTo-Json

Invoke-WebRequest http://localhost:5000/api/auth/register `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

## 🐳 Docker Setup

```bash
# Build and start with docker-compose
docker compose up --build

# In another terminal, initialize database
docker compose exec web flask db upgrade

# View logs
docker compose logs -f
```

## 🎮 Advanced Usage

### Database Migration
```powershell
flask db init          # First time only
flask db migrate -m "Description"
flask db upgrade
```

### Flask Shell (Interactive Testing)
```powershell
flask shell
>>> from models import User
>>> User.query.all()
```

### Running Background Jobs (Celery)
Requires Redis:
```powershell
# In one terminal
celery -A app.celery worker --loglevel=info

# In another terminal
python app.py
```

### Reset Database
```powershell
Remove-Item data.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 🔒 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout (JWT required)
- `POST /api/auth/refresh` - Refresh token

### Students
- `GET /api/students` - List all students
- `POST /api/students` - Create student
- `GET /api/students/<id>` - Get student details
- `PUT /api/students/<id>` - Update student

### Courses
- `GET /api/courses` - List courses
- `POST /api/courses` - Create course
- `GET /api/courses/<id>` - Get course details

### Classes
- `GET /api/classes` - List classes
- `POST /api/classes` - Create class

### Attendance
- `GET /api/attendance` - List attendance records
- `POST /api/attendance` - Mark attendance

### Grades
- `GET /api/grades` - List grades
- `POST /api/grades` - Add/update grade

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Python not found" | Install Python 3.9+ and add to PATH |
| "Module not found" | Activate venv and run `pip install -r requirements.txt` |
| "Port 5000 in use" | Use different port: `python -c "from app import app; app.run(port=8000)"` |
| "No such table" | Initialize DB: `python -c "from app import app, db; app.app_context().push(); db.create_all()"` |
| PowerShell execution error | Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |

For more troubleshooting, see [LOCAL_SETUP.md](LOCAL_SETUP.md#-troubleshooting)

## 📚 Documentation

- [LOCAL_SETUP.md](LOCAL_SETUP.md) - Comprehensive local development guide
- [INFRASTRUCTURE_README.md](INFRASTRUCTURE_README.md) - Production deployment
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Architecture details

## 🔒 Security Notes

- Never commit real secrets or API keys
- `.env` is added to `.gitignore` - keep it local only
- Use strong `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Always use HTTPS in production
- Rotate API keys regularly

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📞 Support

For issues or questions:
1. Check [LOCAL_SETUP.md](LOCAL_SETUP.md#-troubleshooting)
2. Review error messages carefully
3. Verify `.env` configuration
4. Ensure virtual environment is activated

## 📄 License

[Add your license here]

---

**Ready to get started?** 👉 Follow the Quick Start above or see [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed instructions.

**Already running?** Try the test endpoint:
```powershell
Invoke-WebRequest http://localhost:5000/health
```

