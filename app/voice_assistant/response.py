import os
from gtts import gTTS

def respond(response_text):
    try:
        tts = gTTS(text=response_text, lang='ko')
        tts.save("response.mp3")
        os.system("mpg123 response.mp3")
    except Exception as e:
        print(f"응답 생성 중 오류 발생: {e}")
