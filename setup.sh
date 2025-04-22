#!/bin/bash

# Create project directory
mkdir -p college_cafeteria
cd college_cafeteria

# Create necessary directories
mkdir -p templates
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

# Create requirements.txt
echo "Flask==2.0.1
python-dotenv==0.19.0" > requirements.txt

echo "Project structure created successfully!"