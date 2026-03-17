# ⚡ Quick Start Guide

Get the School SaaS app running in **2 minutes** on Windows.

## One-Command Setup

### PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; .\setup.ps1
```

### Command Prompt
```cmd
setup.bat
```

That's it! The script will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Set up database
- ✅ Configure environment

## Then Run

```powershell
python app.py
```

Open browser → **http://localhost:5000/health**

## Next Steps

1. **Read detailed docs**: [LOCAL_SETUP.md](LOCAL_SETUP.md)
2. **Test API**: Try registering a user or checking endpoints
3. **Explore code**: Start with `app.py` → `routes/` package → `models.py`
4. **Make changes**: Files auto-reload during development

## Common Commands

```powershell
# Interactive Python shell for testing
flask shell

# Reset database
Remove-Item data.db

# Run on different port
python -c "from app import app; app.run(port=8000)"

# Start Celery worker (in separate terminal)
make celery-worker  # uses celery_app module

# Deactivate environment
deactivate
```

## Async Tasks with Celery

The app includes Celery for background task processing:

- **Redis** is used as the message broker
- **Example tasks**: Email notifications, report generation, data cleanup
- **API endpoints**: `/api/tasks/test-email`, `/api/tasks/task-status/<task_id>`

### Test Celery

```powershell
# Start Redis (if not using Docker)
redis-server

# Start Celery worker
make celery-worker

# Test email task (in another terminal)
curl -X POST http://localhost:5000/api/tasks/test-email ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_JWT_TOKEN" ^
  -d '{"recipient":"test@example.com","subject":"Test","body":"Hello!"}'
```

## Need Help?

Check [LOCAL_SETUP.md](LOCAL_SETUP.md#-troubleshooting) - it has solutions for common issues.

---

**API is running?** 🎉 Now explore the endpoints in the [README](README.md#-api-endpoints)
