from sqlalchemy import Column, Integer, String, desc, select
from app.database.database import Base, SessionLocal

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column()
    topic = Column(String)

    def __repr__(self):
        return f'{self.id} - {self.topic}'