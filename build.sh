#!/bin/bash
set -e

echo "---- Building Frontend ----"
cd frontend
npm install
npm run build
cd ..

echo "---- Copying build to backend/static ----"
rm -rf backend/static
mkdir -p backend/static
cp -r frontend/build/* backend/static/

echo "Frontend build copied to backend/static"
