SYSTEM_PROMPTS = {
    "default": "당신은 친절한 AI 비서입니다.",
    "teacher": "당신은 교육자이며 학생들을 가르치는 것을 좋아합니다.",
    "friend": "당신은 사용자의 친근한 친구이며 편안한 대화를 나눕니다.",
    "counselor": "당신은 전문 상담가이며 사용자의 고민을 경청하고 조언합니다."
}

def get_chat_messages(prompt_type="default", user_input=""):
    """
    대화 메시지 구성을 생성합니다.
    
    Args:
        prompt_type (str): 사용할 프롬프트 유형 ("default", "teacher", "friend", "counselor")
        user_input (str): 사용자 입력 메시지
    
    Returns:
        list: OpenAI API에 전송할 메시지 목록
    """
    system_prompt = SYSTEM_PROMPTS.get(prompt_type, SYSTEM_PROMPTS["default"])
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

def get_custom_prompt(system_message, user_input):
    """
    사용자 정의 프롬프트를 생성합니다.
    
    Args:
        system_message (str): 시스템 메시지
        user_input (str): 사용자 입력 메시지
    
    Returns:
        list: OpenAI API에 전송할 메시지 목록
    """
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ] 