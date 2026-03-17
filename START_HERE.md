# 🎯 Complete Setup & Troubleshooting Guide

## Welcome! 👋

Your School SaaS application is now fully set up for local development. This guide will help you get started.

## ⚡ TL;DR (Too Long; Didn't Read)

**For PowerShell users:**
```powershell
.\setup.ps1
python app.py
```

**For Command Prompt users:**
```cmd
setup.bat
python app.py
```

Then open: **http://localhost:5000/health**

## 📖 Full Documentation Index

1. **[QUICKSTART.md](QUICKSTART.md)** - 2-minute quick start guide
2. **[LOCAL_SETUP.md](LOCAL_SETUP.md)** - Comprehensive setup with detailed instructions
3. **[VERIFICATION.md](VERIFICATION.md)** - Verify installation is correct
4. **[README.md](README.md)** - API documentation and endpoints

## 🚀 Getting Started

### Step 1: Run Setup (2 minutes)

**Option A: PowerShell (Recommended)**
```powershell
# Open PowerShell in the project folder
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\setup.ps1
```

**Option B: Command Prompt**
```cmd
REM Open Command Prompt in the project folder
setup.bat
```

The setup script will:
- ✅ Create a Python virtual environment
- ✅ Install all dependencies
- ✅ Set up your database
- ✅ Configure environment variables

### Step 2: Verify Setup (1 minute)

```powershell
# PowerShell
.\verify_setup.ps1

# OR Command Prompt
verify_setup.bat
```

This checks everything is installed correctly.

### Step 3: Run the App (1 second)

```powershell
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 4: Test It Works

Open your browser or PowerShell terminal:

```powershell
# Test the health endpoint
Invoke-WebRequest http://localhost:5000/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy"
  }
}
```

## 🧪 Try the API

### Register a User

```powershell
$body = @{
    email = "john@example.com"
    password = "SecurePass123"
    first_name = "John"
    last_name = "Doe"
    user_type = 3
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

$response.Content | ConvertFrom-Json
```

### Login

```powershell
$body = @{
    email = "john@example.com"
    password = "SecurePass123"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Get the token
$token = ($response.Content | ConvertFrom-Json).data.access_token
Write-Host "Token: $token"
```

## 🆘 Troubleshooting

### "Python not found"

**Problem:** `python: command not found` or similar error

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart PowerShell or Command Prompt
4. Try `python --version` again

### "Access to path is denied" (PowerShell)

**Problem:** `File cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

### "ModuleNotFoundError" after setup

**Problem:** `No module named 'flask'` or similar

**Solution:**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # PowerShell
REM venv\Scripts\activate.bat  # Command Prompt

# Reinstall packages
pip install -r requirements.txt
```

### "Port 5000 already in use"

**Problem:** `Address already in use`

**Solution:** Use a different port
```powershell
python -c "from app import app; app.run(port=8000)"
```

Then open: **http://localhost:8000**

### Database errors ("No such table: users")

**Problem:** Database hasn't been initialized

**Solution:**
```powershell
# Delete old database
Remove-Item data.db -ErrorAction SilentlyContinue

# Recreate it
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created!')"

# Start app again
python app.py
```

### Virtual environment won't activate

**Problem:** After running activation command, `(venv)` doesn't appear in terminal

**Solution:**
```powershell
# Check if venv exists
Test-Path venv

# If yes, try explicit path
& "venv/Scripts/Activate.ps1"

# If that fails, check execution policy
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🎮 Useful Commands

### Activate Virtual Environment
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat
```

### Deactivate Virtual Environment
```powershell
deactivate
```

### Run Flask Shell (Interactive Testing)
```powershell
$env:FLASK_APP = 'app.py'
flask shell

# In the shell:
>>> from models import User
>>> User.query.all()
>>> exit()
```

### View All API Routes
```powershell
flask routes
```

### Stop the Server
```
Press Ctrl+C in the terminal
```

### Run on Specific IP/Port
```powershell
python -c "from app import app; app.run(host='0.0.0.0', port=8000)"
```

### Check Python Version
```powershell
python --version
```

### List Installed Packages
```powershell
pip list
```

### View App Logs
```powershell
# Logs are printed to console when running:
python app.py
```

## 📁 Project Structure

```
School_SaaS/
├── app.py                         # Main Flask app
├── config.py                      # Configuration
├── models.py                      # Database models
├── routes.py                      # API endpoints
├── services.py                    # Business logic
├── utils.py                       # Helper functions
├── requirements.txt               # Python packages
│
├── .env                           # ✓ Pre-configured for local dev
├── data.db                        # ✓ Auto-created on first run
├── venv/                          # ✓ Created by setup script
│
├── setup.ps1                      # Automated setup (PowerShell)
├── setup.bat                      # Automated setup (CMD)
├── verify_setup.ps1               # Verify installation (PowerShell)
├── verify_setup.bat               # Verify installation (CMD)
│
├── QUICKSTART.md                  # 👈 Quick start guide
├── LOCAL_SETUP.md                 # 👈 Detailed setup guide
├── VERIFICATION.md                # 👈 Verification guide
├── README.md                      # 👈 API documentation
├── SETUP_COMPLETE.md              # 👈 Summary of changes
└── ... (other files)
```

## ✅ Setup Verification Checklist

After setup, verify:
- [ ] `setup.ps1` or `setup.bat` completed without errors
- [ ] `verify_setup.ps1` or `verify_setup.bat` shows all checks passed
- [ ] `python app.py` starts successfully
- [ ] Health endpoint returns 200: `http://localhost:5000/health`
- [ ] Can see `(venv)` prefix in terminal when environment is active
- [ ] `data.db` file exists in project root

## 🎯 Next Steps

1. **Explore the code** - Start with `app.py`, then `routes.py`, then `models.py`
2. **Test endpoints** - Use the examples above to test registration and login
3. **Make changes** - Edit files; Flask auto-reloads when you save
4. **Read docs** - Check [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed info
5. **Build features** - Add new routes, models, business logic

## 🚨 Emergency Reset

If something goes wrong and you want to start fresh:

```powershell
# Remove everything
Remove-Item venv -Recurse -Force
Remove-Item data.db -Force -ErrorAction SilentlyContinue

# Run setup again
.\setup.ps1

# Or for CMD
# rmdir /s /q venv
# del data.db
# setup.bat
```

## 🔒 Important Security Notes

1. **Never commit `.env`** - It's in `.gitignore` for a reason
2. **Never share your API key** - Keep OPENAI_API_KEY secret
3. **Change SECRET_KEY in production** - Use strong, random values
4. **Use HTTPS in production** - Not needed for local development
5. **Keep database backup** - Consider backing up `data.db`

## 📞 Getting Help

| Question | Answer |
|----------|--------|
| "How do I..." | Check [QUICKSTART.md](QUICKSTART.md) |
| "I'm stuck on setup" | Read [LOCAL_SETUP.md](LOCAL_SETUP.md) |
| "Is everything installed?" | Run `verify_setup.ps1` or `verify_setup.bat` |
| "What endpoints exist?" | See [README.md](README.md#-api-endpoints) |
| "How do I...troubleshoot?" | Check [LOCAL_SETUP.md#-troubleshooting](LOCAL_SETUP.md#-troubleshooting) |

## 🎉 Success!

If you can:
- ✓ Run `python app.py` without errors
- ✓ Access `http://localhost:5000/health`
- ✓ Register a user via the API
- ✓ Login and get a token

**You're ready to develop!** 🚀

---

**Questions?** Check the documentation index at the top of this file.

**Ready to continue?** See [QUICKSTART.md](QUICKSTART.md) for next steps.
