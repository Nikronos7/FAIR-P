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
                response = self.client.models.generate_content(
                    model=current_model,
                    contents=prompt
                )

                # --- SỬA LỖI NONETYPE TẠI ĐÂY ---
                if not response or not response.text:
                    print(
                        f"⚠️ Model {current_model} trả về rỗng, thử model khác...")
                    continue  # Nhảy sang model tiếp theo trong danh sách dự phòng

                text_output = response.text

                # --- BƯỚC LÀM SẠCH ---
                forbidden_tags = ["<blockquote>",
                                  "</blockquote>", "<br>", "</div>"]
                for tag in forbidden_tags:
                    text_output = text_output.replace(tag, "")

                return text_output.strip()

            except Exception as e:
                err_msg = str(e).upper()
                # Nếu hết quota hoặc quá tải, in thông báo rồi CONTINUE để thử model khác
                if any(code in err_msg for code in ["429", "503", "QUOTA", "EXHAUSTED"]):
                    print(f"❌ {current_model} hết lượt, đang chuyển model...")
                    continue

                return f"⚠️ Lỗi hệ thống: {str(e)}"

        return "❤️ Tất cả model AI đều đang bận. Bạn vui lòng đợi 1 phút rồi thử lại nhé!"


chat_logic = ChatBotLogic()
