from catboost import CatBoostClassifier

def load_model(path):
    from_file = CatBoostClassifier()
    model = from_file.load_model(path)
    return model
