# routes/main.py
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models import User, ChatHistory
from app.extensions import db
import openai
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    chat_history = None
    if current_user.is_authenticated:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id)\
            .order_by(ChatHistory.timestamp.desc()).limit(50).all()
    return render_template('index.html', chat_history=chat_history)

@main_bp.route('/get_chat_history')
@login_required
def get_chat_history():
    chat_history = ChatHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ChatHistory.timestamp.desc()).limit(50).all()
    return jsonify([{
        'user_message': chat.user_message,
        'ai_response': chat.ai_response,
        'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for chat in chat_history])

@main_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        message = request.json.get('message')
        
        # ChatGPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 친절한 AI 비서입니다."},
                {"role": "user", "content": message}
            ]
        )
        
        ai_response = response.choices[0].message.content
        
        # 채팅 기록 저장
        chat_history = ChatHistory(
            user_id=current_user.id,
            user_message=message,
            ai_response=ai_response
        )
        db.session.add(chat_history)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "response": ai_response
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
