# Fay Jewelry E-commerce - Docker Setup

This project is containerized using Docker Compose for easy deployment and development.

## 🚀 Quick Start

### Prerequisites
- Docker installed on your system
- Docker Compose installed

### Start the Application

1. **Clone the repository and navigate to the project directory**
   ```bash
   cd /path/to/patrick
   ```

2. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

   For detached mode (running in background):
   ```bash
   docker-compose up --build -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - MongoDB: localhost:27017

### Import Jewelry Data

After the services are running, import the jewelry data:

```bash
# Run the data import script inside the backend container
docker-compose exec backend python import_data.py
```

## 🛠️ Services

### Frontend (Next.js)
- **Container**: `fay-jewelry-frontend`
- **Port**: 3000
- **Build**: Multi-stage Docker build for optimization
- **Features**: React-based e-commerce frontend with Tailwind CSS

### Backend (FastAPI)
- **Container**: `fay-jewelry-backend`
- **Port**: 8000
- **Features**: Python FastAPI with MongoDB integration
- **API Documentation**: http://localhost:8000/docs

### Database (MongoDB)
- **Container**: `fay-jewelry-mongodb`
- **Port**: 27017
- **Features**: MongoDB with authentication and persistent storage

## 📊 Docker Commands

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs frontend
docker-compose logs backend
docker-compose logs mongodb
```

### Stop services
```bash
docker-compose down
```

### Rebuild and restart
```bash
docker-compose up --build --force-recreate
```

### Clean up
```bash
# Remove containers and volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 🔧 Development

### Environment Variables

Backend environment variables (set in docker-compose.yml):
- `MONGODB_URL`: MongoDB connection string
- `PYTHONPATH`: Python path for the application

Frontend environment variables:
- `NEXT_PUBLIC_API_URL`: Backend API URL for client-side calls

### File Structure
```
patrick/
├── docker-compose.yml          # Docker Compose configuration
├── init-mongo.js              # MongoDB initialization script
├── fayjewelry_images/         # Static images volume
├── backend/                   # FastAPI backend
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   └── main.py
└── frontend/                  # Next.js frontend
    ├── Dockerfile
    ├── .dockerignore
    ├── next.config.js
    └── src/
```

## 🔍 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 8000, and 27017 are available
2. **MongoDB connection fails**: Wait for MongoDB healthcheck to pass
3. **Images not loading**: Ensure `fayjewelry_images` directory exists

### Health Checks

All services include health checks:
- MongoDB: Tests database connectivity
- Backend: Tests API availability
- Frontend: Tests web server response

### Volumes

- `mongodb_data`: Persistent MongoDB data storage
- `./fayjewelry_images:/app/images:ro`: Read-only image volume for backend

## 📈 Production Deployment

For production deployment:

1. Update environment variables for security
2. Use proper SSL/TLS certificates
3. Configure reverse proxy (nginx)
4. Set up proper logging and monitoring
5. Use Docker secrets for sensitive data

## 🤝 Contributing

1. Make changes to the codebase
2. Test locally with Docker Compose
3. Ensure all services start correctly
4. Update documentation as needed
