# logic/chatbot.py
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class ChatBotLogic:
    def __init__(self):
        self.api_key = os.getenv("Chat_Bot")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Lỗi Client: {e}")

    def get_response(self, prompt, model_id="models/gemini-flash-latest"):
        if not self.client:
            return "⚠️ Lỗi: Chưa có API Key."

        # Danh sách xoay vòng: Ưu tiên model bạn yêu cầu, sau đó là các bản Flash khác
        model_pool = [model_id, "models/gemini-1.5-flash",
                      "models/gemini-2.5-flash", "models/gemini-flash-lite-latest"]

        # Lọc bỏ trùng lặp
        unique_pool = []
        [unique_pool.append(m) for m in model_pool if m not in unique_pool]

        for current_model in unique_pool:
            try:
                response = self.client.models.generate_content(
                    model=current_model,
                    contents=prompt
                )
                return response.text

            except Exception as e:
                err_msg = str(e)
                # Nếu lỗi hết quota (429) hoặc quá tải (503), hãy thử model tiếp theo
                if any(code in err_msg for code in ["429", "503", "quota"]):
                    continue
                return f"⚠️ Lỗi hệ thống: {err_msg}"

        return "❤️ Tất cả model Flash đều đang bận hoặc hết lượt. Bạn đợi khoảng 1 phút rồi thử lại nhé!"


chat_logic = ChatBotLogic()
