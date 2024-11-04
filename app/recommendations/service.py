import pandas as pd
from sqlalchemy.orm import Session
from app.database.models.feed import Feed
from app.ml.load_models import load_model  # Загрузка модели машинного обучения


model = load_model()

def get_user_recommendations(user_id: int, time: str, posts, users, all_posts, db: Session, limit=10):
    # Получаем посты, которые пользователь уже просмотрел
    user_action_view = db.query(Feed.post_id).filter(Feed.user_id == user_id, Feed.action == "view").all()
    user_action_view = pd.Series(user_action_view).tolist()
    # Определяем посты, которые пользователь не видел
    user_action_not_view = list(set(all_posts) - set(user_action_view))

    # Формируем DataFrame для предсказания
    df = pd.DataFrame({'user_id': user_id, 'post_id': user_action_not_view, 'time': time})
    df = df.merge(posts, how='left', left_on='post_id', right_on='post_id')
    df = df.merge(users, how='left', left_on='user_id', right_on='user_id')

    # Предсказание с помощью ML модели
    pred = pd.DataFrame(model.predict_proba(df.drop(columns=['user_id', 'post_id', 'time']))[:, 1], columns=["predict"])
    df = pd.concat([df, pred], axis=1)
    df = df.sort_values(by=["predict"])

    # Возвращаем список ID рекомендованных постов
    return df["post_id"].tail(limit).tolist()
