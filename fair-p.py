import streamlit as st
from dotenv import load_dotenv

# 1. Khởi động cấu hình
load_dotenv()

st.set_page_config(
    page_title="FAIR-P AI",
    page_icon="assets/fair-p_logo.png",  # Thay icon cũ bằng đường dẫn ảnh logo
    layout="wide"
)
# 2. Định nghĩa cấu trúc trang chuyên nghiệp (Dạng Dictionary)
# Giúp phân nhóm Sidebar rõ ràng
PAGES = {
    "Học tập": [
        st.Page("view/Personal.py", title="Cá Nhân",
                icon=":material/account_circle:"),
        st.Page("view/Skills.py", title="Các kỹ năng",
                icon=":material/explore:"),
    ],
    "Hệ thống": [
        st.Page("view/AboutUs.py", title="Về chúng tôi",
                icon=":material/groups:"),
        st.Page("view/Setting.py", title="Cấu hình",
                icon=":material/settings:"),
    ]
}

# 3. Khởi tạo Điều hướng
pg = st.navigation(PAGES)

pg.run()
