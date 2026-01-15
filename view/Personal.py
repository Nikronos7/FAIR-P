import streamlit as st


def show():  # <--- Bạn phải thêm dòng này
    st.title("👤 Cá Nhân")
    st.write("Chào mừng bạn đến với trang Cá Nhân của FAIR-P!")

    # Ví dụ code xử lý ảnh
    uploaded_file = st.file_uploader(
        "Tải lên ảnh từ vựng của bạn", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        st.image(uploaded_file, caption="Ảnh đã tải lên")
        # Logic AI sẽ viết ở đây...


show()
