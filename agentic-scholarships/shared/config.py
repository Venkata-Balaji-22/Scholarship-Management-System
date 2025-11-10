import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-jwt")
API_PORT = int(os.getenv("API_PORT", "8001"))
FLASK_PORT = int(os.getenv("FLASK_PORT", "5001"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5001,http://localhost:5001").split(",")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
