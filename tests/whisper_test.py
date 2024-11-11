import speech_recognition as sr
from response import respond
from datetime import datetime, timedelta
import re
import tkinter as tk
from tkinter import scrolledtext

class VoiceAssistantGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("음성 비서")
        self.window.geometry("400x300")
        
        self.text_area = scrolledtext.ScrolledText(self.window, width=40, height=15)
        self.text_area.pack(padx=10, pady=10)
        
    def update_text(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.window.update()

def listen_for_wake_word(gui, wake_word="비서야"):

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        gui.update_text("웨이크 워드를 기다리는 중...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ko-KR")
            gui.update_text(f"인식된 텍스트: {text}")
            if wake_word in text:
                gui.update_text("웨이크 워드가 인식되었습니다.")
                respond("넵")
                return True
            else:
                gui.update_text("웨이크 워드가 아닙니다.")
                return False
        except sr.UnknownValueError:
            gui.update_text("명령을 이해할 수 없습니다.")
            return False
        except sr.RequestError as e:
            gui.update_text(f"STT 서비스 에러: {e}")
            return False

def listen_for_command(gui):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        gui.update_text("명령을 말하세요...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="ko-KR")
            gui.update_text(f"명령: {command}")
            return command
        except sr.UnknownValueError:
            gui.update_text("명령을 이해할 수 없습니다.")
            return ""
        except sr.RequestError as e:
            gui.update_text(f"STT 서비스 에러: {e}")
            return ""

def main():
    gui = VoiceAssistantGUI()
    
    def process_voice():
        wake_detected = listen_for_wake_word(gui)
        if wake_detected:
            listen_for_command(gui)
        gui.window.after(100, process_voice)
    
    gui.window.after(100, process_voice)
    gui.window.mainloop()

if __name__ == "__main__":
    main()
