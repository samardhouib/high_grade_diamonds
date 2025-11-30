@echo off
REM Fay Jewelry Docker Startup Script for Windows

echo 🏗️  Building and starting Fay Jewelry services...

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker-compose down

REM Build and start services
echo 🚀 Starting services...
docker-compose up --build -d

REM Wait for services to be healthy
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak > nul

REM Check service health
echo 🔍 Checking service health...

REM Check MongoDB (simplified check)
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ MongoDB is healthy
) else (
    echo ❌ MongoDB health check failed
)

REM Check Backend
powershell -Command "try { Invoke-WebRequest -Uri http://localhost:8000/ -TimeoutSec 5 -UseBasicParsing | Out-Null; Write-Host '✅ Backend API is healthy' } catch { Write-Host '❌ Backend API is not responding' }"

REM Check Frontend
powershell -Command "try { Invoke-WebRequest -Uri http://localhost:3000 -TimeoutSec 5 -UseBasicParsing | Out-Null; Write-Host '✅ Frontend is healthy' } catch { Write-Host '❌ Frontend is not responding' }"

echo.
echo 📊 Services Status:
echo   🌐 Frontend: http://localhost:3000
echo   🔧 Backend API: http://localhost:8000
echo   🗄️  MongoDB: localhost:27017
echo.
echo 📝 To import jewelry data, run:
echo   docker-compose exec backend python import_data.py
echo.
echo 📋 View logs with: docker-compose logs -f
echo 🛑 Stop services with: docker-compose down

pause
