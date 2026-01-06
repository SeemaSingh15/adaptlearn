from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from db.session import Base
from datetime import datetime

class LearningEvent(Base):
    __tablename__ = "learning_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String, index=True) # e.g., 'topic_completed', 'question_answered'
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
