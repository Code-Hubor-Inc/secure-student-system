#!/bin/bash

set -e

echo "Installing project dependencies..."

# Frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Backend dependencies  
echo "Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

echo "All dependencies installed!"