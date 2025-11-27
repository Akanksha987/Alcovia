from .ai_service import AIService
from .database import get_session

get_db = get_session


def get_ai_service() -> AIService:
    return AIService()

