import os
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

        # DANH SÁCH XOAY VÒNG (Pool Model 2026)
        # Ưu tiên model_id được truyền vào (từ Settings), sau đó là các model dự phòng
        model_pool = [
            model_id,                          # Ưu tiên số 1: Model đang chọn
            "models/gemini-flash-latest",      # Dự phòng: Bản mới nhất
            "models/gemini-3-flash-preview",   # Dự phòng: Bản 3.0
            "models/gemini-2.5-flash",         # Dự phòng: Bản ổn định
            "models/gemini-flash-lite-latest"  # Cuối cùng: Bản nhẹ nhất
        ]

        # Lọc bỏ trùng lặp (Giữ nguyên thứ tự ưu tiên)
        unique_pool = []
        [unique_pool.append(m) for m in model_pool if m not in unique_pool]

        for current_model in unique_pool:
            try:
                # Gọi API với model hiện tại trong vòng lặp
                response = self.client.models.generate_content(
                    model=current_model,  # QUAN TRỌNG: Phải dùng current_model, không dùng model_id
                    contents=prompt
                )

                # --- ĐÂY LÀ DÒNG BẠN ĐANG THIẾU ---
                # Biến 'response' được sử dụng ở đây để lấy text
                text_output = response.text

                # --- BƯỚC LÀM SẠCH (CLEANUP) ---
                forbidden_tags = ["<blockquote>",
                                  "</blockquote>", "<br>", "</div>"]
                for tag in forbidden_tags:
                    text_output = text_output.replace(tag, "")

                return text_output.strip()

            except Exception as e:
                err_msg = str(e)
                print(f"⚠️ Lỗi model {current_model}: {err_msg}")

                # Nếu lỗi hết quota (429) hoặc quá tải (503), thử model tiếp theo
                if any(code in err_msg for code in ["429", "503", "quota", "resource_exhausted"]):
                    continue

                # Nếu lỗi khác (như sai API Key), dừng luôn
                return f"⚠️ Lỗi hệ thống: {err_msg}"

        return "❤️ Tất cả model AI đều đang bận. Bạn vui lòng đợi 1 phút rồi thử lại nhé!"


chat_logic = ChatBotLogic()
