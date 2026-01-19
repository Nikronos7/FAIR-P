import streamlit as st
from dotenv import load_dotenv

# 1. Khởi động cấu hình
load_dotenv()

st.set_page_config(
    page_title="FAIR-P AI",
    page_icon="assets/fair-p_logo.png",
    layout="wide"
)

# --- 1. HÀM PHÂN LOẠI GIẤC NGỦ (GIỮ NGUYÊN) ---


def get_quality_options(hours):
    options = {
        "Rất mệt (1)": 1, "Mệt (2)": 2,
        "Buồn ngủ (3)": 3, "Khá buồn ngủ (4)": 4,
        "Tỉnh táo (5)": 5, "Rất tỉnh táo (6)": 6
    }
    all_names = list(options.keys())

    if hours < 4:
        valid_names = all_names[0:2]  # Tệ
    elif 4 <= hours < 6:
        valid_names = all_names[0:4]  # Tệ & Chưa ổn
    elif 6 <= hours <= 9:
        valid_names = all_names[2:6]  # Chưa ổn & Tốt
    else:
        valid_names = all_names[0:4]  # Ngủ quá nhiều (>9h) -> Chưa ổn & Tệ

    return {name: options[name] for name in valid_names}

# --- 2. HÀM PHÂN LOẠI STRESS (LOGIC ĐÃ SỬA CHUẨN) ---


def get_stress_options(has_exercise, duration, level):
    stress_map = {
        "Không có (0)": 0,
        "Thấp - Hơi lo lắng (1)": 1,
        "Khá - Lo lắng (2)": 2,
        "Cao - Rất lo lắng (3)": 3
    }
    all_names = list(stress_map.keys())

    # TRƯỜNG HỢP 1: KHÔNG TẬP THỂ DỤC
    if not has_exercise:
        return stress_map  # Được chọn full mức 0-3

    # TRƯỜNG HỢP 2: CÓ TẬP THỂ DỤC
    # Mặc định: Đã tập là KHÔNG được chọn Stress Cao (3). Max khởi điểm là 2.
    max_idx = 2

    if level == "Nhẹ":
        # Nhẹ >= 60p -> Thấp (1)
        if duration >= 60:
            max_idx = 1
        # Nhẹ < 60p -> Giữ nguyên Khá (2)

    elif level == "Vừa":
        # Vừa >= 60p -> Thấp (1)
        if duration >= 60:
            max_idx = 1
        # Các trường hợp còn lại (<60p) -> Giữ nguyên Khá (2)
        # (Đã loại bỏ logic cho phép Stress Cao khi tập <30p)

    elif level == "Nặng":
        if duration > 45:
            max_idx = 0  # > 45p -> Stress = 0 (Khoá cứng)
        elif duration >= 30:
            max_idx = 1  # 30-45p -> Thấp (1)
        # < 30p -> Giữ nguyên Khá (2)

    # Đảm bảo logic an toàn: Nếu tính toán ra max_idx < 0 thì đưa về 0
    if max_idx < 0:
        max_idx = 0

    valid_names = all_names[0:max_idx + 1]
    return {name: stress_map[name] for name in valid_names}

# --- 3. GIAO DIỆN CHỐT CHẶN (HEALTH GATE) ---


def show_health_gate():
    st.title("🛡️ Cổng Kiểm Soát Sức Khỏe FAIR-P")
    st.info(
        "Chào Nikronos7! Hãy cập nhật trạng thái để AI tối ưu hóa lộ trình học cho bạn.")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🌙 Chỉ số Giấc ngủ")
            sleep_hours = st.slider(
                "Số giờ ngủ đêm qua:", 0.0, 12.0, 8.0, 0.25, format="%g giờ")

            q_options = get_quality_options(sleep_hours)
            q_names = list(q_options.keys())
            # Logic chọn mặc định thông minh: Luôn chọn cái tốt nhất trong list
            q_name = st.select_slider(
                "Cảm giác khi thức dậy:", options=q_names, value=q_names[-1])
            q_score = q_options[q_name]

        with col2:
            st.subheader("🏋️ Vận động & Tâm trạng")
            has_ex = st.toggle("Bạn đã tập thể dục hôm nay?")

            ex_duration = 0
            ex_level = "Nhẹ"

            # Chỉ hiện input vận động khi Toggle được bật
            if has_ex:
                c1, c2 = st.columns(2)
                ex_duration = c1.number_input(
                    "Thời gian (phút):", 5, 180, 30, step=5)
                ex_level = c2.select_slider(
                    "Cường độ:", ["Nhẹ", "Vừa", "Nặng"])

            # Lấy danh sách options từ logic mới
            s_options = get_stress_options(has_ex, ex_duration, ex_level)
            s_names = list(s_options.keys())

            st.write("Mức độ Stress hiện tại:")

            # --- KHẮC PHỤC LỖI RANGE ERROR (QUAN TRỌNG) ---
            # Nếu danh sách chỉ có 1 lựa chọn (ví dụ: chỉ còn mức 0)
            if len(s_names) == 1:
                st.success(
                    f"✅ Tuyệt vời! Bài tập {ex_level} {ex_duration}p đã giúp bạn loại bỏ hoàn toàn stress.")
                s_name = s_names[0]  # Lấy giá trị duy nhất đó
                s_score = s_options[s_name]
            else:
                # Nếu có từ 2 lựa chọn trở lên thì mới hiện Slider
                default_val = s_names[0] if has_ex else s_names[1]
                # Kiểm tra lại default_val có nằm trong s_names không để tránh lỗi
                if default_val not in s_names:
                    default_val = s_names[0]

                s_name = st.select_slider(
                    "Chọn mức độ:",  # Label ẩn đi cho gọn
                    options=s_names,
                    value=default_val,
                    label_visibility="collapsed"
                )
                s_score = s_options[s_name]

            if has_ex:
                st.caption(
                    f"✨ FAIR-P giới hạn mức Stress tối đa dựa trên bài tập {ex_level}.")

        if st.button("🚀 XÁC NHẬN & VÀO HÀNH TRÌNH HỌC", use_container_width=True):
            st.session_state.user_data = {
                "sleep_hours": sleep_hours,
                "sleep_quality": q_score,
                "stress_score": s_score,
                "has_exercise": has_ex,
                "exercise_detail": f"{ex_level} {ex_duration}p" if has_ex else "Không"
            }
            st.session_state.health_submitted = True
            st.balloons()
            st.rerun()


# --- LOGIC ĐIỀU HƯỚNG ---
if 'health_submitted' not in st.session_state:
    st.session_state.health_submitted = False

if not st.session_state.health_submitted:
    show_health_gate()


# 2. Định nghĩa cấu trúc trang chuyên nghiệp (GIỮ NGUYÊN CỦA BẠN)
if st.session_state.health_submitted == True:
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
    with st.sidebar:
        # Sử dụng Expander để thu gọn thông tin
        with st.expander("❤️ Trạng thái sức khỏe", expanded=False):
            data = st.session_state.user_data

            # Hiển thị các chỉ số với Icon sinh động
            st.write(f"🌙 Ngủ: **{data['sleep_hours']}h**")
            st.caption(f"Chất lượng: {data['sleep_quality']}/6")

            st.write(f"🧠 Stress: **{data['stress_score']}/3**")
            st.write(f"🏋️ Vận động: **{data['exercise_detail']}**")

            # Nút nhập lại đặt trong Expander để Sidebar sạch sẽ hơn
            if st.button("🔄 Cập nhật lại", use_container_width=True):
                st.session_state.health_submitted = False
                st.rerun()
