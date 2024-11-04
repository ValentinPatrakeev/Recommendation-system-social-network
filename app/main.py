from fastapi import FastAPI
from app.recommendations import router
from config.settings import settings  # Импорт настроек

app = FastAPI()

# Подключаем роутер для работы с постами
app.include_router(router.router)

# Главная страница для проверки работы API
@app.get("/")
def root():
    return {"message": f"API is working in {settings.environment} mode"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
