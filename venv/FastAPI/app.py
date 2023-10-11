from typing import List
import os
from datetime import datetime
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
#from database import SessionLocal, engine
from sqlalchemy import Column, Integer, String, desc, select, func, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
from sqlalchemy.orm import relationship
from schema import PostGet, Response
import joblib, pickle
import hashlib


#DATABASE
SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@" \
                          "postgres.lab.karpov.courses:6432/startml"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#POST
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column()
    topic = Column(String)

    def __repr__(self):
        return f'{self.id} - {self.topic}'

#USER
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)

#FEED
class Feed(Base):
    __tablename__ = "feed_action"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    action = Column(String)
    time = Column(DateTime)
    user = relationship(User)
    post = relationship(Post)

#LOAD FEATURES
def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 1000
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn,
                                       chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
        print(chunk_dataframe)
    conn.close()
    data = pd.concat(chunks, ignore_index=True)

    return data


def load_features() -> pd.DataFrame:
    query = "v_patrakeev_all_posts_new"
    query2 = "v_patrakeev_all_users_new"
    return batch_load_sql(query), batch_load_sql(query2)


# Loading data by posts and users
posts, users = load_features()
#posts, users = pd.read_csv("../post_feature_to_SQL_new", sep=";"),pd.read_csv("../user_feature_to_SQL_new", sep=";")

all_posts = list(posts['post_id'])

def get_exp_group(user_id: int) -> str:
    part = int(hashlib.md5((str(user_id) + 'salt').encode()).hexdigest(),16)% 100
    if part >= 50:
        exp_group = 'test'
    else: exp_group = 'control'
    return exp_group

def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":  # проверяем где выполняется код в лмс, или локально. Немного магии
        if exp_group == 'test':
            MODEL_PATH = '/workdir/user_input/model_test'
        else: MODEL_PATH = '/workdir/user_input/model_control'
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    model_path_control = get_model_path("../model_first_LogReg.pkl")
    model_path_test = get_model_path("../model_second_catboost")
    from_file = CatBoostClassifier()
    model_control = joblib.load(model_path_control)
    model_test = from_file.load_model(model_path_test)
    return model_control, model_test

model_control, model_test = load_models()


app=FastAPI()
def get_db():
    return SessionLocal() #Создаем сессию при вызове функции get_db


@app.get("/post/recommendations/", response_model=Response)
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

        exp_group = get_exp_group(id)
        if exp_group == 'control':
            model = model_control
        elif exp_group == 'test':
            model = model_test
        else:
            raise ValueError('unknown group')

        pred = pd.DataFrame(model.predict_proba(df.drop(columns=['user_id','post_id', 'time']))[:, 1], columns=["predict"])
        df = pd.concat([df, pred], axis=1)
        df = df.sort_values(by=["predict"])

        spisok = df["post_id"].tail(limit).tolist()
        for x in range(len(spisok)):
            spisok[x] = int(spisok[x])

        result = Response(**{'exp_group':exp_group, 'recommendations':db.query(Post).filter(Post.id.in_(spisok)).limit(limit).all()})
        db.close()
        engine.dispose()

        return result
    else:
        raise HTTPException(404)



