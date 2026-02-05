from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import router
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Password Security Service",
    description=(
        "Микросервис оценки надёжности паролей. "
        "Пароли не сохраняются и не логируются."
    ),
    version="1.0"
)

# Отключаем логирование тела запросов
logging.getLogger("uvicorn.access").disabled = True

app.include_router(router)

@app.exception_handler(Exception)
async def safe_exception_handler(request: Request, exc: Exception):
    """
    Глобальный обработчик ошибок.
    Исключает утечку чувствительных данных.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Внутренняя ошибка сервиса"
        }
    )