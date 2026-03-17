# 🚀 School SaaS - Local Development Setup Guide

This guide will help you set up and run the School SaaS application on your local Windows machine.

## 📋 Prerequisites

Before you start, ensure you have:

- **Python 3.9 or higher** - [Download here](https://www.python.org/downloads/)
  - Make sure to check **"Add Python to PATH"** during installation
- **Git** (optional) - [Download here](https://git-scm.com/)
- **Code editor** - VS Code recommended, but any editor works

## ⚡ Quick Start (Automated)

### For Windows PowerShell Users:

1. Open PowerShell in the project directory
2. Run the setup script:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   .\setup.ps1
   ```

### For Windows Command Prompt Users:

1. Open Command Prompt in the project directory
2. Run the setup script:
   ```cmd
   setup.bat
   ```

These scripts will automatically:
- Create a Python virtual environment
- Install all dependencies
- Initialize the database
- Set up environment variables

Then skip to **Step 5** below.

---

## 📝 Manual Setup (Step-by-Step)

If you prefer manual setup or the scripts don't work:

### Step 1: Create Virtual Environment

Open PowerShell or Command Prompt in the project directory and run:

```powershell
# PowerShell
python -m venv venv
```

```cmd
# Command Prompt
python -m venv venv
```

### Step 2: Activate Virtual Environment

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` prefix in your terminal.

### Step 3: Upgrade pip

```powershell
# PowerShell or Command Prompt
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Create .env File

Copy the .env file (it's pre-configured for local development):

```powershell
# Already created - just verify it exists
cat .env
```

The `.env` file should contain default values for SQLite database and development settings.

### Step 6: Initialize Database

**Option A: Using Flask-Migrate (Recommended)**

```powershell
$env:FLASK_APP = 'app.py'
flask db init        # Only needed once
flask db migrate -m "Initial migration"
flask db upgrade
```

**Option B: Direct Database Creation**

```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created!')"
```

This will create `data.db` in the project root.

### Step 7: Run the Application

```powershell
python app.py
```

You should see output like:
```
 * Serving Flask app 'app.py'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open your browser and go to **http://localhost:5000** to access the API.

---

## 🧪 Testing the API

### Health Check Endpoint

Test if the API is running:

```powershell
# PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET

# Or using curl (if available)
curl http://localhost:5000/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "message": "School SaaS API is running"
  }
}
```

### Create a Test User (Registration)

```powershell
$body = @{
    email = "test@example.com"
    password = "testpassword123"
    first_name = "John"
    last_name = "Doe"
    user_type = 3
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/auth/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

### Login

```powershell
$body = @{
    email = "test@example.com"
    password = "testpassword123"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

---

## 📁 Project Structure

```
School_SaaS/
├── app.py                 # Flask application entry point
├── config.py              # Configuration management
├── models.py              # Database models
├── routes.py              # API endpoints
├── services.py            # Business logic
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local)
├── data.db               # SQLite database (created after setup)
├── venv/                 # Virtual environment (created after setup)
└── ... (other files)
```

---

## 🔧 Useful Commands

### Run Flask Development Server
```powershell
python app.py
```

### Run with Specific Port
```powershell
python -c "from app import app; app.run(port=8000)"
```

### Enter Flask Shell (for testing)
```powershell
flask shell
```

### Create Database Backup
```powershell
Copy-Item data.db data.db.backup
```

### Reset Database
```powershell
Remove-Item data.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Deactivate Virtual Environment
```powershell
deactivate
```

---

## 🐛 Troubleshooting

### Issue: "Python is not recognized as an internal or external command"

**Solution:** Python is not in your PATH. Add it:
1. Reinstall Python
2. Make sure to check "Add Python to PATH" during installation
3. Or manually add Python to PATH in System Environment Variables

### Issue: Virtual environment won't activate

**Solution:** Change PowerShell execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Make sure virtual environment is activated and dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Issue: "No such table: users"

**Solution:** Initialize database:
```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Issue: Port 5000 already in use

**Solution:** Use a different port:
```powershell
python -c "from app import app; app.run(port=8000)"
```

---

## 🎯 Next Steps

After successful setup:

1. **Explore the API** - Check out `/api/auth`, `/api/students`, `/api/courses`
2. **Review the code** - Start with `app.py`, then `routes.py` and `models.py`
3. **Make changes** - Edit files and the Flask dev server will hot-reload
4. **Use Flask Shell** - Test database queries interactively:
   ```powershell
   flask shell
   >>> from models import User
   >>> User.query.all()
   ```

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## 💡 Tips for Local Development

1. **Keep a terminal open** - One for the Flask server, another for commands
2. **Use Flask shell** - Test your models and business logic interactively
3. **Check .env file** - Most issues come from missing/wrong environment variables
4. **Use `--reload`** - Flask auto-reloads when you save files
5. **Read error messages** - They usually tell you exactly what's wrong

---

## ❓ Need Help?

If you encounter issues:

1. Check the error message carefully
2. Look at the Troubleshooting section above
3. Verify `.env` file is set correctly
4. Make sure virtual environment is activated
5. Try running the setup script again

Good luck! 🚀
