from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.llm_service import llm_service
from core.deps import get_current_user
from models.user import User

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

from sqlalchemy.orm import Session
from db.session import get_db
from models.learning_event import LearningEvent

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Log the learning event
    event = LearningEvent(
        user_id=current_user.id,
        event_type="chat_interaction",
        details={"message_length": len(request.message)}
    )
    db.add(event)
    db.commit()
    
    response_text = await llm_service.generate_text(request.message)
    return ChatResponse(response=response_text)

class QuizRequest(BaseModel):
    context: str

# Allow returning raw JSON dict
@router.post("/quiz")
async def generate_quiz_endpoint(request: QuizRequest, current_user: User = Depends(get_current_user)):
    import json
    json_str = await llm_service.generate_quiz(request.context)
    try:
        data = json.loads(json_str)
        return data
    except:
        return {
            "question": "Could not generate quiz from context.",
            "options": ["Retry"],
            "correct_answer": 0,
            "explanation": "Internal parsing error."
        }

from sqlalchemy import func
from datetime import datetime, timedelta

@router.get("/progress")
def get_user_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get last 7 days activity
    seven_days_ago = datetime.utcnow() - timedelta(days=6)
    
    # Query for daily counts
    daily_counts = db.query(
        func.date(LearningEvent.created_at).label('date'),
        func.count(LearningEvent.id).label('count')
    ).filter(
        LearningEvent.user_id == current_user.id,
        LearningEvent.created_at >= seven_days_ago
    ).group_by(
        func.date(LearningEvent.created_at)
    ).all()
    
    # Format for chart (fill missing days with 0)
    data_map = {str(d[0]): d[1] for d in daily_counts}
    
    labels = []
    data_points = []
    
    for i in range(7):
        date = (datetime.utcnow() - timedelta(days=6-i)).date()
        date_str = str(date)
        labels.append(date.strftime("%a")) # Mon, Tue...
        data_points.append(data_map.get(date_str, 0))
        
    return {
        "labels": labels,
        "data": data_points
    }
