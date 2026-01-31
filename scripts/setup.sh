
### **scripts/setup.sh**
```bash
#!/bin/bash

set -e  # Exit on any error

echo " Setting up Secure Student System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW} $1${NC}"
}

print_error() {
    echo -e "${RED} $1${NC}"
}

# Check prerequisites
check_prerequisite() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 not found. Please install $1"
        exit 1
    fi
    print_status "$1 found: $(command -v $1)"
}

echo "🔍 Checking prerequisites..."
check_prerequisite "node"
check_prerequisite "npm"
check_prerequisite "python3"
check_prerequisite "docker"
check_prerequisite "docker-compose"

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
if [ $NODE_MAJOR -lt 18 ]; then
    print_error "Node.js version 18+ required. Current: $NODE_VERSION"
    exit 1
fi
print_status "Node.js version: $NODE_VERSION"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
if [ $PYTHON_MAJOR -lt 3 ] || [ $PYTHON_MAJOR -eq 3 -a $PYTHON_MINOR -lt 9 ]; then
    print_error "Python 3.9+ required. Current: $PYTHON_VERSION"
    exit 1
fi
print_status "Python version: $PYTHON_VERSION"

# Frontend setup
echo "Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
    print_status "Frontend dependencies installed"
else
    print_status "Frontend dependencies already exist"
fi
cd ..

# Backend setup
echo "Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Python virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
if [ ! -f "requirements_installed" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    touch requirements_installed
    print_status "Backend dependencies installed"
else
    print_status "Backend dependencies already installed"
fi

# Create environment files if they don't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Created .env file from example. Please configure it."
else
    print_status ".env file already exists"
fi

cd ..

# Create root environment file
if [ ! -f ".env" ]; then
    cat > .env << EOL
# Secure Student System Environment Configuration
# Copy this file to .env.production for production deployment

# Application
APP_NAME=Secure Student System
APP_ENV=development
DEBUG=true

# URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@localhost:5432/secure_student

# Security
SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE=104857600  # 100MB in bytes
UPLOAD_DIR=./storage/uploads

# Redis
REDIS_URL=redis://localhost:6379

# Email (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EOL
    print_warning "Created root .env file. Please configure it for your environment."
fi

# Make scripts executable
chmod +x scripts/*.sh

print_status "Setup complete!"
echo ""
echo " Next steps:"
echo "1. Configure your .env files in both frontend/ and backend/ directories"
echo "2. Run: docker-compose up -d  to start the database and services"
echo "3. Run: npm run dev  to start development servers"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo " For more details, see docs/GETTING_STARTED.md"