from pydantic import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    port: int = 8000
    database_url: str
    load_from_db: bool = False  # Флаг для загрузки из базы данных
    posts_csv_path: str = "./data/post_feature_to_SQL_new.csv"  # Путь по умолчанию для постов
    users_csv_path: str = "./data/user_feature_to_SQL_new.csv"  # Путь по умолчанию для пользователей
    posts_table_name: str = "v_patrakeev_all_posts_new"  # Название таблицы для постов
    users_table_name: str = "v_patrakeev_all_users_new"  # Название таблицы для пользователей
    catboost_model_path = "app/ml/models/model_second_catboost"
    logreg_model_path = "app/ml/models/logreg_model.pkl"

    ml_model: str

    class Config:
        env_file = ".env"

settings = Settings()
