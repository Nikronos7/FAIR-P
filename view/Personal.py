import streamlit as st
from logic.gemini_ai import chat_logic

st.set_page_config(page_title="Cá Nhân", layout="wide")

# 1. SIDEBAR: Lựa chọn tính năng
# Vì bạn đã có các page, đoạn này sẽ tự động xuất hiện dưới danh sách page
with st.sidebar:
    # Dùng st.radio có sẵn của Streamlit, không cần import thêm
    selected = st.sidebar.radio(
        "Các mục điều hướng:",
        ["Học tập", "Dashboard", "Tiến trình"],
        index=0  # Mặc định là Học tập
    )

# 2. PHÂN CHIA NỘI DUNG CHÍNH
if selected == "Học tập":

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sử dụng khung container để chia khu vực chat
    chat_container = st.container(height=450, border=True)

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Bạn muốn tìm hiểu gì?..."):
        # Lưu và hiển thị ngay lập tức
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Gọi logic AI và hiển thị
        response = chat_logic.get_response(prompt)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        st.rerun()

elif selected == "Dashboard":
    st.subheader("📊 Bảng điều khiển phân tích")
    st.info("Bảng theo dõi tiến độ học tập.")

elif selected == "Tiến trình":
    st.subheader("📈 Theo dõi lộ trình cá nhân")
    st.write("Tiến độ ôn tập:")
    st.progress(60)
