from app.models import ChatHistory
from app.extensions import db
from app.voice_assistant.prompts import get_chat_messages

class VoiceAssistantGUI:
    def __init__(self):
        self.chat_history = []
        self.prompt_type = "default"
    
    def get_gpt_response(self, user_input):
        try:
            messages = get_chat_messages(self.prompt_type, user_input)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response_text = response.choices[0].message.content
            self.update_text(f"AI: {response_text}")
            
            # 채팅 기록 저장
            chat_history = ChatHistory(
                user_id=current_user.id,
                user_message=user_input,
                ai_response=response_text
            )
            db.session.add(chat_history)
            db.session.commit()
            
            return response_text
        except Exception as e:
            error_msg = f"GPT 응답 생성 중 오류 발생: {e}"
            self.update_text(error_msg)
            return error_msg

    def speak_response(self, response_text):
        try:
            tts = gTTS(text=response_text, lang='ko')
            tts.save("response.mp3")
            os.system("mpg123 response.mp3")
        except Exception as e:
            self.update_text(f"음성 출력 중 오류 발생: {e}")

    def set_prompt_type(self, prompt_type):
        """
        AI 비서의 성격을 변경합니다.
        
        Args:
            prompt_type (str): "default", "teacher", "friend", "counselor" 중 하나
        """
        if prompt_type in ["default", "teacher", "friend", "counselor"]:
            self.prompt_type = prompt_type
            self.update_text(f"AI 비서의 성격이 변경되었습니다: {prompt_type}")
        else:
            self.update_text("지원하지 않는 프롬프트 타입입니다.")