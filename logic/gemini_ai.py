import os
from dotenv import load_dotenv
from google import genai
from logic.prompts import LEARNING_CHATBOT_PROMPT, GENERAL_ASSISTANT_PROMPT

# Load biến môi trường
load_dotenv()


class GeminiLogic:
    def __init__(self, service_type="Chatbot"):
        # Lựa chọn Key dựa trên mục đích sử dụng
        if service_type == "Chatbot":
            api_key = os.getenv("Chat_Bot")
            self.system_instruction = LEARNING_CHATBOT_PROMPT
        else:
            api_key = os.getenv("Assistant")
            self.system_instruction = GENERAL_ASSISTANT_PROMPT

        # Khởi tạo Client với Key tương ứng
        self.client = genai.Client(api_key=api_key)

    def get_response(self, user_input):
        try:
            response = self.client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=user_input,
                config={
                    "system_instruction": self.system_instruction
                }
            )
            return response.text
        except Exception as e:
            return f"Lỗi hệ thống AI: {str(e)}"


# Khởi tạo một instance mặc định cho Chatbot
chat_logic = GeminiLogic(service_type="Chatbot")
