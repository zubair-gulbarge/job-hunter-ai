from pathlib import Path

PROJECT_NAME = "job-hunter-ai"

directories = [
    f"{PROJECT_NAME}/backend/app/api",
    f"{PROJECT_NAME}/backend/app/core",
    f"{PROJECT_NAME}/backend/app/models",
    f"{PROJECT_NAME}/backend/app/services",
    f"{PROJECT_NAME}/backend/app/templates",
    f"{PROJECT_NAME}/frontend",
]

files = {
    f"{PROJECT_NAME}/backend/app/main.py":
        "# FastAPI/Flask application entry point\n",

    f"{PROJECT_NAME}/backend/app/api/__init__.py": "",
    f"{PROJECT_NAME}/backend/app/core/__init__.py": "",
    f"{PROJECT_NAME}/backend/app/models/__init__.py": "",
    f"{PROJECT_NAME}/backend/app/services/__init__.py": "",
    f"{PROJECT_NAME}/backend/app/templates/.gitkeep": "",

    f"{PROJECT_NAME}/backend/requirements.txt":
        "# Python dependencies\n",

    f"{PROJECT_NAME}/backend/Dockerfile":
        "# Backend Dockerfile\n",

    f"{PROJECT_NAME}/.env.example":
        """# Environment Variables

OPENAI_API_KEY=
MONGODB_URI=
DATABASE_NAME=job_hunter_ai
""",

    f"{PROJECT_NAME}/.gitignore":
        """# Python
__pycache__/
*.pyc
.venv/
venv/

# Environment
.env

# Node
node_modules/

# Build
dist/
build/

# OS
.DS_Store
""",

    f"{PROJECT_NAME}/docker-compose.yml":
        """version: '3.9'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"

  frontend:
    image: node:20
    working_dir: /app
    ports:
      - "3000:3000"

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
""",

    f"{PROJECT_NAME}/README.md":
        "# Job Hunter AI\n\nAI-powered resume and job application assistant.\n",
}


def create_project():
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    # Create files
    for file_path, content in files.items():
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.write_text(content, encoding="utf-8")

    print(f"✅ Project structure '{PROJECT_NAME}' created successfully!")


if __name__ == "__main__":
    create_project()
