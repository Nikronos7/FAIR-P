import streamlit as st
from dotenv import load_dotenv
from data.User_Data.User_data import verify_login, get_guest_data
# 1. Khởi động cấu hình
load_dotenv()

st.set_page_config(
    page_title="FAIR-P AI",
    page_icon="assets/fair-p_logo.png",
    layout="wide"
)

# --- 1. HÀM PHÂN LOẠI GIẤC NGỦ ---


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

# --- 2. HÀM PHÂN LOẠI STRESS ---


def get_stress_options(has_exercise, duration, level):
    stress_map = {
        "Không có (0)": 0, "Thấp - Hơi lo lắng (1)": 1,
        "Khá - Lo lắng (2)": 2, "Cao - Rất lo lắng (3)": 3
    }
    all_names = list(stress_map.keys())

    if not has_exercise:
        return stress_map

    max_idx = 2
    if level == "Nhẹ":
        if duration >= 60:
            max_idx = 1
    elif level == "Vừa":
        if duration >= 60:
            max_idx = 0
        elif duration >= 45:
            max_idx = 1
        else:
            max_idx = 2
    elif level == "Nặng":
        if duration >= 45:
            max_idx = 0
        elif duration >= 30:
            max_idx = 1
        else:
            max_idx = 2

    if max_idx < 0:
        max_idx = 0
    valid_names = all_names[0:max_idx + 1]
    return {name: stress_map[name] for name in valid_names}
# --- 3. HÀM CẬP NHẬT VẬN ĐỘNG (POP-UP) ---


@st.dialog("🏋️ Cập nhật Vận động Giữa giờ")
def show_exercise_dialog():
    st.write("Cập nhật bài tập để AI điều chỉnh mức Stress giới hạn.")

    col1, col2 = st.columns(2)
    with col1:
        new_duration = st.number_input(
            "Vừa tập thêm (phút):", 5, 120, 15, step=5)
    with col2:
        new_level = st.selectbox("Cường độ:", ["Nhẹ", "Vừa", "Nặng"])

    if st.button("Xác nhận & Cập nhật", use_container_width=True):
        # 1. Lấy dữ liệu cũ
        d = st.session_state.user_data

        # 2. Cộng dồn thời gian
        old_duration = d.get('exercise_duration', 0)
        total_duration = old_duration + new_duration

        # 3. Cập nhật điểm số vận động (để vẽ biểu đồ Radar)
        level_to_score = {"Nhẹ": 1.0, "Vừa": 1.5, "Nặng": 2.0}

        # 4. TÍNH LẠI STRESS (LOGIC MỚI: KẸP TRẦN)
        # Lấy danh sách các mức stress hợp lệ cho bài tập này
        # Ví dụ: Nhẹ 30p -> Trả về {0:0, 1:1, 2:2} -> List values là [0, 1, 2]
        new_stress_options = get_stress_options(
            True, total_duration, new_level)
        valid_scores = list(new_stress_options.values())

        # Tìm mức "Max trong khoảng slide bar" (Mức tệ nhất cho phép)
        # Ví dụ: Nhẹ 30p -> Max cho phép là 2 (Khá)
        max_allowed_stress = max(valid_scores)

        # Lấy stress hiện tại của người dùng
        current_stress = d.get('stress_score', 2)

        # So sánh:
        # - Nếu đang Stress 3 (Cao) > Max 2 -> Bị kéo xuống 2.
        # - Nếu đang Stress 1 (Thấp) < Max 2 -> Giữ nguyên 1.
        new_stress_score = min(current_stress, max_allowed_stress)

        # 5. Cập nhật vào Session State
        st.session_state.user_data.update({
            "has_exercise": True,
            "exercise_level": new_level,
            "exercise_duration": total_duration,
            "exercise_score": level_to_score[new_level],
            "exercise_detail": f"{new_level} (Tổng {total_duration}p)",
            "stress_score": new_stress_score  # Cập nhật stress mới
        })

        # 6. Thông báo
        st.session_state.toast_msg = f"Đã cộng thêm {new_duration}p tập! Stress giới hạn ở mức {new_stress_score}. 📉"
        st.rerun()
# --- 4. GIAO DIỆN CHỐT CHẶN (HEALTH GATE) ---


def show_health_gate():
    # --- Lấy tên người dùng ---

    st.title("🛡️ Cổng Kiểm Soát Sức Khỏe FAIR-P")
    account_info = st.session_state.get('account_info', {})
    display_name = account_info.get('username', 'Bạn')

    # --- ĐỊNH NGHĨA ĐIỂM SỐ VẬN ĐỘNG (Dùng cho tính toán AI sau này) ---
    level_to_score = {
        "Nhẹ": 1.0,
        "Vừa": 1.5,
        "Nặng": 2.0
    }

    # --- LOGIC LẤY GIÁ TRỊ MẶC ĐỊNH (KHI BẤM CẬP NHẬT) ---
    defaults = {
        "sleep": 8.0,
        "water": 0.5,
        "has_ex": False,
        "ex_time": 30,
        "ex_level": "Nhẹ"
    }
    if 'user_data' in st.session_state:
        d = st.session_state.user_data
        defaults["sleep"] = d.get("sleep_hours", 8.0)
        defaults["water"] = d.get("water_consumed", 0.5)
        defaults["has_ex"] = d.get("has_exercise", False)
        # Nếu muốn nhớ chi tiết Ex_level cũ, cần lưu riêng biến, tạm thời để mặc định là Nhẹ

    st.info(
        f"Chào {display_name}! Hãy cập nhật trạng thái để AI tối ưu hóa lộ trình học cho bạn.")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🌙 Giấc ngủ & 💧 Nước")
            # 1. Slide chọn nước
            water_liters = st.slider(
                "Lượng nước đã uống (Lít):", 0.0, 4.0, defaults["water"], 0.1)

            st.divider()

            # 2. Slide giấc ngủ
            sleep_hours = st.slider(
                "Số giờ ngủ đêm qua:", 0.0, 12.0, defaults["sleep"], 0.25, format="%g giờ")
            q_options = get_quality_options(sleep_hours)
            q_names = list(q_options.keys())
            q_name = st.select_slider(
                "Cảm giác khi thức dậy:", options=q_names, value=q_names[-1])
            q_score = q_options[q_name]

        with col2:
            st.subheader("🏋️ Vận động & Tâm trạng")
            has_ex = st.toggle("Bạn đã tập thể dục hôm nay?",
                               value=defaults["has_ex"])

            ex_duration = 0
            ex_level = "Nhẹ"

            if has_ex:
                c1, c2 = st.columns(2)
                ex_duration = c1.number_input(
                    "Thời gian (phút):", 5, 180, 30, step=5)
                ex_level = c2.select_slider(
                    "Cường độ:", ["Nhẹ", "Vừa", "Nặng"])

            s_options = get_stress_options(has_ex, ex_duration, ex_level)
            s_names = list(s_options.keys())

            st.write("Mức độ Stress hiện tại:")
            if len(s_names) == 1:
                st.success(
                    f"✅ Tuyệt vời! Bài tập {ex_level} {ex_duration}p đã loại bỏ stress.")
                s_name = s_names[0]
                s_score = s_options[s_name]
            else:
                default_val = s_names[0] if has_ex else s_names[1]
                if default_val not in s_names:
                    default_val = s_names[0]
                s_name = st.select_slider(
                    "Chọn mức độ:", options=s_names, value=default_val, label_visibility="collapsed")
                s_score = s_options[s_name]

            if has_ex:
                st.caption(
                    f"✨ FAIR-P giới hạn mức Stress tối đa dựa trên bài tập {ex_level}.")

        # Nút xác nhận
        btn_label = "✅ BẮT ĐẦU HỌC"

        if st.button(btn_label, use_container_width=True):
            # --- TÍNH TOÁN ĐIỂM SỐ VẬN ĐỘNG ---
            current_ex_score = level_to_score[ex_level] if has_ex else 0.0

            st.session_state.user_data = {
                "sleep_hours": sleep_hours,
                "sleep_quality": q_score,
                "water_consumed": water_liters,
                "stress_score": s_score,
                "has_exercise": has_ex,
                "exercise_level": ex_level,
                "exercise_duration": ex_duration,
                "exercise_score": current_ex_score,
                "exercise_detail": f"{ex_level} {ex_duration}p" if has_ex else "Không"
            }
            st.session_state.health_submitted = True
            st.balloons()
            st.rerun()

# --- 5. GIAO DIỆN ĐĂNG NHẬP (MỚI THÊM) ---


def render_login():
    st.title("🛡️ FAIR-P SYSTEM ACCESS")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Đăng nhập")
            username = st.text_input(
                "Tên đăng nhập", placeholder="nhập tên của bạn")
            password = st.text_input("Mật khẩu", type="password")

            if st.button("🚀 ĐĂNG NHẬP", type="primary", use_container_width=True):
                success, user_info = verify_login(username, password)
                if success:
                    st.session_state.is_logged_in = True
                    # [QUAN TRỌNG] Load dữ liệu cũ vào user_data để HealthGate hiển thị lại
                    # Nếu user mới thì để rỗng để nhập từ đầu
                    st.session_state.user_data = user_info.get(
                        'daily_status', {})
                    # Lưu thêm thông tin tài khoản để hiển thị tên
                    st.session_state.account_info = user_info.get(
                        'account', {})
                    st.session_state.db_grades = user_info.get(
                        'learning_results', {}).get('grades', [])
                    st.rerun()
                else:
                    st.error("Sai thông tin đăng nhập!")

        with col2:
            st.markdown("### Khách truy cập")
            st.info(
                "Trải nghiệm nhanh các tính năng mà không cần lưu trữ dữ liệu lâu dài.")
            if st.button("👤 DÙNG THỬ (GUEST)", use_container_width=True):
                # [FIX] Gọi hàm lấy dữ liệu Guest từ User_data.py
                guest_data = get_guest_data()
                st.session_state.is_logged_in = True
                st.session_state.user_data = guest_data.get('daily_status', {})
                st.session_state.account_info = guest_data.get('account', {})
                st.session_state.db_grades = guest_data.get(
                    'learning_results', {}).get('grades', [])
                st.rerun()


# --- LOGIC ĐIỀU KHIỂN CHÍNH (ĐÃ BỌC ĐĂNG NHẬP) ---

# 1. Khởi tạo trạng thái đăng nhập
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# 2. Kiểm tra: Chưa đăng nhập -> Hiện Login
if not st.session_state.is_logged_in:
    render_login()

# 3. Đã đăng nhập -> Chạy luồng App cũ của bạn (KHÔNG ĐỔI)
else:
    # --- Code cũ của bạn bắt đầu từ đây ---
    if 'health_submitted' not in st.session_state:
        st.session_state.health_submitted = False

    if not st.session_state.health_submitted:
        show_health_gate()

    # --- GIAO DIỆN CHÍNH ---
    if st.session_state.health_submitted == True:
        # [LƯU Ý] Đảm bảo tên file trong view khớp với thư mục của bạn
        PAGES = {
            "Học tập": [
                st.Page("view/Personal.py", title="Cá nhân",
                        icon=":material/dashboard:"),
                st.Page("view/Skills.py", title="Các kỹ năng",
                        icon=":material/explore:"),
            ],
            "Hệ thống": [
                st.Page("view/Setting.py", title="Cấu hình",
                        icon=":material/settings:"),
                st.Page("view/AboutUs.py", title="Về chúng tôi",
                        icon=":material/groups:"),
            ]
        }
        pg = st.navigation(PAGES)
        pg.run()

        # --- SIDEBAR CẢI TIẾN ---
        with st.sidebar:
            st.divider()
            # 1. LOGIC TOAST
            if 'toast_msg' in st.session_state and st.session_state.toast_msg:
                st.toast(st.session_state.toast_msg)
                st.session_state.toast_msg = None

            # 2. TRẠNG THÁI SỨC KHỎE (Code cũ giữ nguyên)
            with st.expander("❤️ Trạng thái & Nước", expanded=False):
                data = st.session_state.user_data  # Data này đã được HealthGate nạp

                # Hiển thị Hydration
                water_val = data.get('water_consumed', 0.0)
                st.write(f"💧 Nước: **{water_val:.2f} Lít**")
                target_water = 3.0
                progress = min(water_val / target_water, 1.0)
                st.progress(progress)

                if progress >= 1.0:
                    st.caption("✅ Đã đạt mục tiêu nước!")
                else:
                    st.caption(
                        f"Thiếu {(target_water - water_val):.1f}L mục tiêu.")

                st.divider()

                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"🌙 Ngủ: **{data.get('sleep_hours', 0)}h**")
                    st.caption(f"Q: {data.get('sleep_quality', 0)}/6")
                with col_b:
                    st.write(f"🧠 Stress: **{data.get('stress_score', 0)}/3**")
                    st.caption(f"VĐ: {data.get('exercise_detail', 'Không')}")

                st.divider()

                # Nút cộng nước
                if st.button("➕ Uống thêm 250ml (0.25L)", use_container_width=True):
                    st.session_state.user_data['water_consumed'] = water_val + 0.25
                    st.session_state.toast_msg = "Đã nạp thêm 0.25L nước! 💧"
                    st.rerun()

                if st.button("🏋️ Cập nhật Vận động", use_container_width=True):
                    show_exercise_dialog()
