# EnnovateX AI Platform - Deployment Guide

This guide provides comprehensive instructions for deploying the EnnovateX AI Platform in various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Cloud Deployment](#cloud-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Node.js**: Version 18 or higher (for local development)
- **Python**: Version 3.11 or higher (for local development)
- **Git**: Latest version

### Hardware Requirements

#### Minimum (Development)
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB free space

#### Recommended (Production)
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+ SSD
- Network: Stable internet connection

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ennovatex-ai-platform-redesign
```

### 2. Environment Variables

Copy the environment templates and configure them:

```bash
# Backend environment
cp backend/.env.example backend/.env
cp .env.production backend/.env.production

# Frontend environment
cp .env.example .env.local
cp .env.production .env.production
```

### 3. Configure Environment Variables

Edit the environment files with your specific values:

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ennovatex
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# AI Models
HUGGINGFACE_API_KEY=your-huggingface-key
OPENAI_API_KEY=your-openai-key

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=50MB
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_ENVIRONMENT=development
```

## Local Development

### Quick Start

Use the deployment script for easy setup:

```bash
# Deploy locally with build and logs
./scripts/deploy.sh local --build --logs
```

### Manual Setup

#### 1. Start Infrastructure Services

```bash
# Start PostgreSQL and Redis
docker-compose -f backend/docker-compose.yml up -d postgres redis
```

#### 2. Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

## Production Deployment

### Docker Deployment

#### 1. Build and Deploy

```bash
# Build and deploy all services
./scripts/deploy.sh production --build
```

#### 2. Manual Docker Deployment

```bash
# Build images
docker-compose -f docker-compose.fullstack.yml build

# Deploy services
docker-compose -f docker-compose.fullstack.yml up -d

# Check status
docker-compose -f docker-compose.fullstack.yml ps
```

### Server Setup

#### 1. Prepare Production Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
sudo apt install nginx -y
```

#### 2. Configure Nginx

```bash
# Copy Nginx configuration
sudo cp config/nginx.conf /etc/nginx/nginx.conf

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

#### 3. SSL Certificate Setup

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Environment Configuration

#### Production Environment Variables

Update `.env.production` files with production values:

```bash
# Backend
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:password@postgres:5432/ennovatex_prod
REDIS_URL=redis://:password@redis:6379
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Frontend
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXT_PUBLIC_APP_URL=https://yourdomain.com
NEXT_PUBLIC_ENVIRONMENT=production
```

## Cloud Deployment

### Vercel (Frontend)

#### 1. Setup

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### 2. Environment Variables

Set in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_APP_URL`
- `NEXT_PUBLIC_ENVIRONMENT`

### Railway/Render (Backend)

#### Railway

1. Connect GitHub repository
2. Set environment variables
3. Deploy from `backend` directory
4. Configure custom domain

#### Render

1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### AWS/GCP/Azure

#### Container Services

- **AWS**: ECS, EKS, or App Runner
- **GCP**: Cloud Run, GKE, or App Engine
- **Azure**: Container Instances, AKS, or App Service

#### Database Services

- **AWS**: RDS PostgreSQL, ElastiCache Redis
- **GCP**: Cloud SQL, Memorystore
- **Azure**: Database for PostgreSQL, Cache for Redis

## CI/CD Pipeline

### GitHub Actions

The repository includes a complete CI/CD pipeline (`.github/workflows/deploy.yml`) that:

1. **Tests**: Runs frontend and backend tests
2. **Builds**: Creates Docker images
3. **Deploys**: Deploys to staging and production
4. **Notifies**: Sends deployment notifications

### Setup

1. **Repository Secrets**:
   ```
   DEPLOY_HOST=your-server-ip
   DEPLOY_USER=your-server-user
   DEPLOY_KEY=your-ssh-private-key
   DB_PASSWORD=your-database-password
   REDIS_PASSWORD=your-redis-password
   SLACK_WEBHOOK=your-slack-webhook-url
   ```

2. **Environments**:
   - Create `staging` and `production` environments in GitHub
   - Configure protection rules and required reviewers

### Manual Deployment

```bash
# Deploy to staging
git push origin staging

# Deploy to production
git push origin main
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs -f

# Health endpoints
curl http://localhost:8000/health
curl http://localhost:3000/api/health
```

### Monitoring Stack

The deployment includes:

- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and visualization
- **Elasticsearch**: Log aggregation
- **Kibana**: Log analysis

### Backup Strategy

#### Database Backup

```bash
# Create backup
docker exec postgres pg_dump -U user ennovatex > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker exec -i postgres psql -U user ennovatex < backup_file.sql
```

#### Automated Backups

```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

### Updates and Maintenance

```bash
# Update application
git pull origin main
./scripts/deploy.sh production --pull

# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean up Docker resources
docker system prune -f
```

## Troubleshooting

### Common Issues

#### 1. Port Conflicts

```bash
# Check port usage
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000

# Kill process using port
sudo kill -9 $(sudo lsof -t -i:3000)
```

#### 2. Database Connection Issues

```bash
# Check database status
docker-compose exec postgres pg_isready

# Check database logs
docker-compose logs postgres

# Reset database
docker-compose down
docker volume rm $(docker volume ls -q | grep postgres)
docker-compose up -d postgres
```

#### 3. Memory Issues

```bash
# Check memory usage
docker stats

# Increase Docker memory limit
# Docker Desktop: Settings > Resources > Memory

# Clean up unused resources
docker system prune -a
```

#### 4. SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

### Logs and Debugging

```bash
# Application logs
docker-compose logs -f frontend
docker-compose logs -f backend

# System logs
sudo journalctl -u nginx
sudo journalctl -u docker

# Real-time monitoring
docker stats
htop
```

### Performance Optimization

#### Frontend
- Enable compression in Nginx
- Use CDN for static assets
- Implement caching strategies
- Optimize images and assets

#### Backend
- Configure connection pooling
- Implement Redis caching
- Optimize database queries
- Use async/await patterns

#### Database
- Regular VACUUM and ANALYZE
- Proper indexing
- Connection pooling
- Read replicas for scaling

## Security Considerations

### Production Security Checklist

- [ ] Use strong passwords and secrets
- [ ] Enable SSL/TLS encryption
- [ ] Configure firewall rules
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] Access logging and monitoring
- [ ] Rate limiting and DDoS protection
- [ ] Regular security audits

### Security Headers

The Nginx configuration includes:
- HSTS (HTTP Strict Transport Security)
- CSP (Content Security Policy)
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection

## Support

For deployment issues:

1. Check this documentation
2. Review application logs
3. Check GitHub Issues
4. Contact the development team

---

**Last Updated**: $(date +%Y-%m-%d)
**Version**: 1.0.0