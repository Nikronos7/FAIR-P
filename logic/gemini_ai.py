from google import genai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Khởi tạo client một lần khi cần và cache bằng st.cache_resource để tránh khởi tạo mỗi lần rerun


@st.cache_resource
def _get_gemini_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_gemini_response(user_input, system_instruction):
    try:
        client = _get_gemini_client()
        response = client.models.generate_content(
            model="gemini-3-flash-preview",  # Hoặc gemini-2.0-flash-exp nếu có
            config={"system_instruction": system_instruction},
            contents=user_input,
        )
        return response.text
    except Exception as e:
        return f"Lỗi kết nối AI: {str(e)}"
