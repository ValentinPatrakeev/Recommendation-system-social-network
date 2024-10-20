import pandas as pd
from sqlalchemy.orm import Session
from app.database.database import engine
from config.settings import settings  # Импортируем настройки


def batch_load_sql(query: str) -> pd.DataFrame:
    """
    Функция для загрузки данных из базы данных частями (batch loading).
    """
    CHUNKSIZE = 1000
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []

    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)

    conn.close()
    data = pd.concat(chunks, ignore_index=True)

    return data


def load_features_from_db() -> (pd.DataFrame, pd.DataFrame):
    """
    Функция для загрузки признаков для пользователей и постов из базы данных.
    """
    query_posts = f"SELECT * FROM {settings.posts_table_name}"  # SQL запрос для постов
    query_users = f"SELECT * FROM {settings.users_table_name}"  # SQL запрос для пользователей

    posts = batch_load_sql(query_posts)
    users = batch_load_sql(query_users)

    return posts, users


def load_features_from_csv(posts_path: str, users_path: str) -> (pd.DataFrame, pd.DataFrame):
    """
    Функция для загрузки признаков из CSV файлов.
    """
    posts = pd.read_csv(posts_path, sep=";")
    users = pd.read_csv(users_path, sep=";")

    return posts, users


def load_features() -> (pd.DataFrame, pd.DataFrame):
    """
    Главная функция для загрузки данных в зависимости от флага LOAD_FROM_DB.
    Если флаг True, данные загружаются из базы данных, иначе из CSV.
    """
    if settings.load_from_db:
        return load_features_from_db()
    else:
        posts_path = settings.posts_csv_path
        users_path = settings.users_csv_path
        return load_features_from_csv(posts_path, users_path)
