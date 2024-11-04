# load_features.py
import pandas as pd
from sqlalchemy.orm import Session


from app.database.database import engine
from config.settings import settings

class FeatureLoader:
    def __init__(self):
        self._posts_cache = None
        self._users_cache = None

    def batch_load_sql(self, query: str) -> pd.DataFrame:
        CHUNKSIZE = 1000
        conn = engine.connect().execution_options(stream_results=True)
        chunks = [chunk for chunk in pd.read_sql(query, conn, chunksize=CHUNKSIZE)]
        conn.close()
        return pd.concat(chunks, ignore_index=True)

    def load_features_from_db(self) -> (pd.DataFrame, pd.DataFrame):
        query_posts = f"SELECT * FROM {settings.posts_table_name}"
        query_users = f"SELECT * FROM {settings.users_table_name}"
        posts = self.batch_load_sql(query_posts)
        users = self.batch_load_sql(query_users)
        return posts, users

    def load_features_from_csv(self, posts_path: str, users_path: str) -> (pd.DataFrame, pd.DataFrame):
        posts = pd.read_csv(posts_path, sep=";")
        users = pd.read_csv(users_path, sep=";")
        return posts, users

    def load_features(self) -> (pd.DataFrame, pd.DataFrame):
        if self._posts_cache is None or self._users_cache is None:
            if settings.load_from_db:
                self._posts_cache, self._users_cache = self.load_features_from_db()
            else:
                posts_path = settings.posts_csv_path
                users_path = settings.users_csv_path
                self._posts_cache, self._users_cache = self.load_features_from_csv(posts_path, users_path)
        return self._posts_cache, self._users_cache

# Создаем единственный экземпляр класса
feature_loader = FeatureLoader()
