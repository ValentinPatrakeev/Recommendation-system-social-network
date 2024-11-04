from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.recommendations.service import get_user_recommendations
from app.database.models.post import Post
from app.recommendations.load_features import feature_loader
router = APIRouter()

@router.get("/post/recommendations/")
def recommended_post(id: int, time: str, limit: int = 10, db: Session = Depends(get_db)):
    posts, users = feature_loader.load_features()
    all_posts = list(posts['post_id'])
    if id in users["user_id"].values:
        # Получаем список рекомендованных постов для пользователя
        spisok = get_user_recommendations(id, time, posts, users, all_posts, db, limit=limit)
        result = db.query(Post).filter(Post.id.in_(spisok)).limit(limit).all()
        return result
    else:
        raise HTTPException(404, detail="User not found")
