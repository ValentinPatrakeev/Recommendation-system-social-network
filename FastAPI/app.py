from typing import List
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import Base, SessionLocal
from schema import PostGet
from table_post import Post
from table_user import User
from table_feed import Feed
from load_models import load_model
from load_features import load_features

#Создаем экземпляр фреймворка API
app=FastAPI()

#Создаем сессию при вызове функции get_db
def get_db():
    return SessionLocal()

#Загружаем наши признаки для модели с севера
##posts, users = load_features()
##либо загружаем локально
posts, users = pd.read_csv("../data csv/post_feature_to_SQL_new", sep=";"),pd.read_csv("../data csv/user_feature_to_SQL_new", sep=";")

#создадим список наших постов (список ID всех постов, что мы распологаем)
all_posts = list(posts['post_id'])

#загружаем нашу модель
model = load_model("../Models/model_second_catboost")

#Запускаем наш сервис
@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_post(id: int, time: str, limit: int=10, db: Session = Depends(get_db), all_posts=all_posts):

    if id in users["user_id"].values:
        user_action_view = db.query(Feed.post_id).filter(Feed.user_id == id, Feed.action == "view").all()
        user_action_view = pd.Series(user_action_view ).tolist()
        user_action_not_view = list(set(all_posts) - set(user_action_view))
        df = pd.DataFrame({'user_id': id,
                           'post_id': user_action_not_view,
                           'time': time})

        df = df.merge(posts, how='left', left_on='post_id', right_on='post_id')
        df = df.merge(users, how='left', left_on='user_id', right_on='user_id')

        pred = pd.DataFrame(model.predict_proba(df.drop(columns=['user_id','post_id', 'time']))[:, 1], columns=["predict"])
        df = pd.concat([df, pred], axis=1)
        df = df.sort_values(by=["predict"])

        spisok = df["post_id"].tail(limit).tolist()
        for x in range(len(spisok)):
            spisok[x] = int(spisok[x])
        result = db.query(Post).filter(Post.id.in_(spisok)).limit(limit).all()
        db.close()

        return result
    else:
        raise HTTPException(404)



