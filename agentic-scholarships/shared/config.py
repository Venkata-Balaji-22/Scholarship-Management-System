import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-jwt")
API_PORT = int(os.getenv("API_PORT", "8000"))
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
# Allow the frontend (8080), Flask auth (5000) and FastAPI (8000) during local development
ALLOWED_ORIGINS = os.getenv(
	"ALLOWED_ORIGINS",
	"http://127.0.0.1:8080,http://localhost:8080,http://127.0.0.1:5000,http://localhost:5000,http://127.0.0.1:8000",
).split(",")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
