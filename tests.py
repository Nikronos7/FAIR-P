import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("Chat_Bot"))

print("--- DANH SÁCH MODELS KHẢ DỤNG ---")
# Lấy danh sách tất cả các model mà API Key này có quyền truy cập
for model in client.models.list():
    # Chỉ lọc các model hỗ trợ tạo nội dung (generateContent)
    if "generateContent" in model.supported_actions:
        print(f"Model Name: {model.name}")
        print(f"Display Name: {model.display_name}")
        print("-" * 30)
