# ✅ Installation Verification Checklist

After running setup, use this checklist to verify everything is working correctly.

## Pre-Installation Requirements

- [ ] Python 3.9 or higher installed
  ```powershell
  python --version
  ```
  Should output: `Python 3.9.x` or higher

## Post-Installation Verification

### 1. Virtual Environment Created
```powershell
# Check if venv folder exists
Test-Path venv
```
Should output: `True`

### 2. Dependencies Installed
```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Check pip packages
pip list | grep -i flask
```
Should show Flask and other packages installed

### 3. Database Created
```powershell
# Check if database file exists
Test-Path data.db
```
Should output: `True`

### 4. Flask App Runs
```powershell
# Start the server
python app.py
```
Should output something like:
```
 * Serving Flask app 'app.py'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 5. API Health Check
In a different terminal:
```powershell
# Check if API is responding
Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET
```
Should return JSON with status: healthy

## Common Issues & Solutions

### Issue: "Python was not found"
**Solution:**
1. Reinstall Python from https://www.python.org/
2. IMPORTANT: Check "Add Python to PATH" during installation
3. Restart your terminal

### Issue: Virtual environment won't activate
**Solution:**
```powershell
# Check execution policy
Get-ExecutionPolicy

# If it says "Restricted", run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activation again
.\venv\Scripts\Activate.ps1
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```powershell
# Make sure venv is activated - check for (venv) prefix in terminal
# Then reinstall requirements
pip install -r requirements.txt
```

### Issue: Database table errors
**Solution:**
```powershell
# Delete old database
Remove-Item data.db

# Recreate it
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created!')"
```

### Issue: Port 5000 is already in use
**Solution:**
```powershell
# Use a different port
python -c "from app import app; app.run(port=8000)"

# Then access at http://localhost:8000
```

## Environment File Verification

Check that `.env` file exists and contains:

```powershell
# View .env file
cat .env
```

Should show variables like:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///data.db
```

## Running Tests

### Test 1: Register a User
```powershell
$body = @{
    email = "test@example.com"
    password = "password123"
    first_name = "Test"
    last_name = "User"
    user_type = 3
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/auth/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

### Test 2: Login
```powershell
$body = @{
    email = "test@example.com"
    password = "password123"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

Should return a token in the response.

### Test 3: Flask Shell
```powershell
flask shell
# In the Python shell:
>>> from models import User
>>> User.query.all()
# Should return a list of users (even if empty [])
>>> exit()
```

## Useful Debugging Commands

```powershell
# Check Python path
python -c "import sys; print(sys.executable)"

# List all installed packages
pip list

# Show Flask app info
flask --app app shell

# View Flask config
flask --app app shell
>>> from app import app
>>> app.config

# Test database connection
python -c "from app import db; print('Database connected:', db.engine)"

# Check what blueprints are registered
flask --app app shell
>>> from app import app
>>> for rule in app.url_map.iter_rules(): print(rule)
```

## Performance Baseline

After setup, your app should:
- ✅ Start in < 2 seconds
- ✅ Respond to /health in < 100ms
- ✅ Register user in < 500ms
- ✅ Login in < 500ms

If it's significantly slower, check:
1. Antivirus/firewall interference
2. Disk I/O performance
3. System resources (RAM, CPU)

## Success Indicators

You know setup is complete when:
- ✅ No errors in terminal when running `python app.py`
- ✅ `/health` endpoint returns 200 OK
- ✅ Can register a new user via `/api/auth/register`
- ✅ Can login and receive a JWT token
- ✅ `.env` file exists with correct settings
- ✅ `data.db` file exists

## Next Steps

Once verified:
1. Review [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed information
2. Check [QUICKSTART.md](QUICKSTART.md) for common commands
3. Explore API endpoints in [README.md](README.md#-api-endpoints)
4. Start coding! 🚀

## Getting Help

If verification fails:
1. Run setup script again: `.\setup.ps1` or `setup.bat`
2. Check for error messages - they usually explain the issue
3. Compare your environment with the Prerequisites section
4. See [LOCAL_SETUP.md#-troubleshooting](LOCAL_SETUP.md#-troubleshooting)

---

**Everything working?** 🎉 Check out the [API endpoints](README.md#-api-endpoints) to start building!
