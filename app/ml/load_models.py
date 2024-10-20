from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
import joblib
import os
from config.settings import settings

# Пути к моделям зашиты в коде
CATBOOST_MODEL_PATH = "./models/model_second_catboost"
LOGREG_MODEL_PATH = "./models/logreg_model.pkl"

def load_catboost_model() -> CatBoostClassifier:
    """
    Загружает модель CatBoost из зашитого пути.
    """
    model = CatBoostClassifier()
    model.load_model(f'app/ml/models/model_second_catboost')
    return model

def load_logreg_model() -> LogisticRegression:
    """
    Загружает модель логистической регрессии (LogReg) из зашитого пути.
    """
    return joblib.load("app/ml/models/logreg_model.pkl")

def load_model():
    """
    Загружает модель в зависимости от флага model_name в настройках.
    """
    if settings.ml_model == "cat_boost":
        return load_catboost_model()
    elif settings.ml_model == "log_reg":
        return load_logreg_model()
    else:
        raise ValueError(f"Model {settings.model_name} is not supported")
