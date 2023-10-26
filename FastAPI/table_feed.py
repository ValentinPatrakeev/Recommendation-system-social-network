from sqlalchemy import ForeignKey, desc, func, select, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
from table_post import Post
from table_user import User

class Feed(Base):
    __tablename__ = "feed_action"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    action = Column(String)
    time = Column(DateTime)
    user = relationship(User)
    post = relationship(Post)