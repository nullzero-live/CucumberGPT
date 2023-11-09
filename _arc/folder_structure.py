import os
from pathlib import Path

# Define the directory structure
dirs = [
    "./docs",
    "./src/api/routers",
    "./src/core",
    "./src/models",
    "./src/utils",
    "./tests",
    "./.github/workflows",
    "./node_modules/cypress",
    "./node_modules/cucumber-preprocessor",
    "./frontend",
    "./db/mongo_data",
    "./db/qdrant_data",
]

# Define the files to be created with placeholder content
files = {
    "./docs/README.md": "# Project README\n\nThis is the README file for the project.",
    "./docs/CONTRIBUTING.md": "# Contributing Guidelines\n\nGuidelines for contributing to the project.",
    "./src/main.py": "# Main application entry point\n",
    "./.env": "# Environment variables\n",
    "./Dockerfile": "# Dockerfile for building the application image\n",
    "./docker-compose.yml": "# Docker Compose configuration\n",
    "./frontend/streamlit_app.py": "# Streamlit application script\n",
}

# Create directories
for dir in dirs:
    Path(dir).mkdir(parents=True, exist_ok=True)

# Create files
for file_path, content in files.items():
    file = Path(file_path)
    file.write_text(content)

print("Directory structure and files created successfully.")
