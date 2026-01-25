import streamlit as st
from dotenv import load_dotenv
from data.User_Data.User_data import verify_login, get_guest_data
from logic.calculations import calculate_single_activity_score
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
# --- 3. HÀM CẬP NHẬT SỨC KHOẺ & VẬN ĐỘNG (POP-UP) ---


def add_water_callback():
    # 1. Khởi tạo biến tạm để gom số nước (nếu chưa có)
    if 'temp_water_added' not in st.session_state:
        st.session_state.temp_water_added = 0.0

    # 2. Cộng dồn vào biến tạm (Ví dụ bấm 3 lần thì biến này thành 0.75)
    st.session_state.temp_water_added += 0.25

    # 3. Cập nhật dữ liệu thật
    current_val = st.session_state.user_data.get('water_consumed', 0.0)
    new_total = current_val + 0.25
    st.session_state.user_data['water_consumed'] = new_total

    # 4. Ghi thông báo dựa trên BIẾN TẠM (Hiển thị tổng số đã bấm)
    added_total = st.session_state.temp_water_added
    st.session_state.toast_msg = f"➕ Đã nạp thêm tổng cộng: {added_total:.2f}L 💧"


def reset_exercise_callback():
    """Reset vận động và giữ nguyên Dialog"""
    st.session_state.daily_activities = {}
    st.session_state.user_data.update({
        'exercise_score': 0.0,
        'exercise_detail': "Không",
        'has_exercise': False,
        'stress_score': 2  # Reset về mức trung bình
    })

# --- DIALOG CHÍNH ---


@st.dialog("❤️ TRẠNG THÁI & VẬN ĐỘNG")
def show_health_status_dialog():
    # 1. Khởi tạo Dictionary nếu chưa có
    if 'daily_activities' not in st.session_state:
        st.session_state.daily_activities = {}

    tab_overview, tab_exercise = st.tabs(
        ["📊 Tổng quan", "🏋️ Cập nhật Vận động"])

    # ==================================================
    # TAB 1: TỔNG QUAN (Xử lý nước bằng Callback)
    # ==================================================
    with tab_overview:
        st.markdown("### 💧 Hydration")
        # Lấy data real-time
        current_water = st.session_state.user_data.get('water_consumed', 0.0)
        target_water = 3.0

        c1, c2 = st.columns([2, 1], vertical_alignment="bottom")
        with c1:
            st.metric("Đã uống", f"{current_water:.2f}L",
                      delta=f"{current_water - target_water:.2f}L")
        with c2:
            # QUAN TRỌNG: Dùng on_click gọi hàm callback bên ngoài
            # Không dùng st.fragment hay st.rerun() ở đây -> Dialog sẽ không bị tắt
            st.button("➕ 0.25L", key="btn_water_dialog",
                      on_click=add_water_callback)

        if st.button("🔄 Cập nhật", key="btn_refresh_app", use_container_width=True):
            st.rerun()

        progress = min(current_water / target_water, 1.0)
        st.progress(progress, text=f"Mục tiêu: {target_water}L")

        if progress >= 1.0:
            st.caption("✅ Đã đạt mục tiêu nước!")

        st.divider()

        # Phần ngủ & Stress
        data = st.session_state.user_data
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"🌙 Ngủ: **{data.get('sleep_hours', 0)}h**")
        with col_b:
            s_val = data.get('stress_score', 0)
            color = {0: "green", 1: "blue",
                     2: "orange", 3: "red"}.get(s_val, "red")
            st.markdown(f"🧠 Stress: :{color}[**{s_val}/3**]")

    # ==================================================
    # TAB 2: VẬN ĐỘNG (Logic Cộng Dồn Thông Minh)
    # ==================================================
    with tab_exercise:
        st.info("💡 Các bài tập sẽ được cộng dồn điểm (Tối đa 2.0/ngày).")

        # A. HIỂN THỊ DANH SÁCH (LOGGING)
        current_acts = st.session_state.daily_activities
        if current_acts:
            st.write("📌 **Chi tiết hôm nay:**")
            for act_name, info in current_acts.items():
                st.write(
                    f"• {act_name}: {info['duration']}p - {info['intensity']} ({info['score']}đ)")

        st.divider()

        # B. FORM NHẬP LIỆU
        sport_list = [
            "Đi bộ", "Yoga/Thiền", "Chạy bộ", "Gym/Calisthenics",
            "Bóng đá", "Bơi lội", "Khác"
        ]

        # Mapping để lọc cường độ hợp lý cho từng môn
        intensity_map = {
            "Đi bộ": ["Nhẹ", "Vừa"],
            "Yoga/Thiền": ["Nhẹ", "Vừa"],
            # Các môn còn lại mặc định có Vừa/Cao
        }

        activity = st.selectbox("Môn thể thao", sport_list)
        # Tự động lấy list cường độ, nếu không có trong map thì lấy list mặc định
        available_int = intensity_map.get(
            activity, ["Vừa", "Cao (High Intensity)"])

        c_time, c_int = st.columns(2)
        with c_time:
            duration = st.number_input(
                "Thời gian (phút)", min_value=15, value=30, step=5)
        with c_int:
            intensity = st.selectbox("Cường độ", available_int)

        # C. XỬ LÝ LOGIC (SMART ACCUMULATION)
        c_btn_add, c_btn_reset = st.columns([2, 1])

        with c_btn_add:
            if st.button("💾 Lưu bài tập", type="primary", use_container_width=True):
                # 1. Tính điểm bài tập mới (Dùng hàm chuẩn)
                new_points = calculate_single_activity_score(intensity)

                # 2. Logic Cộng Dồn (Smart Update)
                if activity in st.session_state.daily_activities:
                    # Nếu môn này đã có -> Cộng dồn vào
                    old_data = st.session_state.daily_activities[activity]
                    updated_duration = old_data['duration'] + duration
                    updated_score = old_data['score'] + new_points

                    # Cập nhật lại vào Dictionary
                    st.session_state.daily_activities[activity] = {
                        # Ghi chú lịch sử cường độ
                        "intensity": f"{old_data['intensity']} + {intensity}",
                        "duration": updated_duration,
                        "score": updated_score
                    }
                    action_msg = f"Đã cộng thêm {duration}p vào {activity}"
                else:
                    # Nếu chưa có -> Tạo mới
                    st.session_state.daily_activities[activity] = {
                        "intensity": intensity,
                        "duration": duration,
                        "score": new_points
                    }
                    action_msg = f"Đã thêm mới: {activity}"

                # 3. Tính Tổng Điểm Toàn Cục (Re-calculate Global Score)
                # Cộng tổng điểm của tất cả các môn trong dictionary
                raw_total_score = sum(
                    item['score'] for item in st.session_state.daily_activities.values())

                # GIỚI HẠN TRẦN (MAX CAP): 2.0 ĐIỂM
                final_score = min(raw_total_score, 2.0)

                # 4. Tạo chuỗi hiển thị tóm tắt
                # Ví dụ: "Đi bộ (Nhẹ + Vừa) + Gym (Cao)"
                detail_parts = []
                for k, v in st.session_state.daily_activities.items():
                    detail_parts.append(f"{k} ({v['duration']}p)")
                detail_str = " + ".join(detail_parts)

                # 5. Logic Giảm Stress (Tự động tìm mức tốt nhất)
                # Quét lại toàn bộ hoạt động để tìm bài tập nặng nhất
                min_stress_limit = 2
                all_intensities_str = " ".join(
                    [v['intensity'] for v in st.session_state.daily_activities.values()])
                total_duration = sum(
                    [v['duration'] for v in st.session_state.daily_activities.values()])

                # Nếu có bất kỳ bài Cao nào hoặc tổng thời gian > 60p -> Xả stress tối đa
                if "Cao" in all_intensities_str or total_duration >= 60:
                    min_stress_limit = 0
                elif "Vừa" in all_intensities_str or total_duration >= 30:
                    min_stress_limit = min(min_stress_limit, 1)

                current_stress = st.session_state.user_data.get(
                    'stress_score', 2)
                final_stress = min(current_stress, min_stress_limit)

                # 6. Commit vào Database (User Data)
                st.session_state.user_data.update({
                    'exercise_score': final_score,  # Đảm bảo max 2.0
                    'exercise_detail': detail_str,
                    'has_exercise': True,
                    'stress_score': final_stress
                })

                st.session_state.toast_msg = f"{action_msg}. Tổng điểm: {final_score}/2.0"
                st.rerun()

        with c_btn_reset:
            # Dùng Callback để reset mà không tắt Dialog (nếu muốn)
            # Tuy nhiên nút này ít dùng nên để rerun cũng được, nhưng dùng on_click cho xịn
            st.button("Reset", use_container_width=True,
                      on_click=reset_exercise_callback)

# --- 4. GIAO DIỆN CHỐT CHẶN (HEALTH GATE) ---


def show_health_gate():
    st.title("🛡️ Cổng Kiểm Soát Sức Khỏe FAIR-P")
    account_info = st.session_state.get('account_info', {})
    display_name = account_info.get('username', 'Bạn')

    # Cấu hình môn thể thao (Copy để đồng bộ logic)
    sport_config = {
        "Đi bộ": ["Nhẹ", "Vừa"],
        "Yoga/Thiền": ["Nhẹ", "Vừa"],
        "Chạy bộ": ["Vừa", "Cao (High Intensity)"],
        "Gym/Calisthenics": ["Vừa", "Cao (High Intensity)"],
        "Bóng đá": ["Vừa", "Cao (High Intensity)"],
        "Bơi lội": ["Vừa", "Cao (High Intensity)"],
        "Khác": ["Nhẹ", "Vừa", "Cao (High Intensity)"]
    }

    # Giá trị mặc định
    defaults = {
        "sleep": st.session_state.user_data.get("sleep_hours", 8.0),
        "water": st.session_state.user_data.get("water_consumed", 0.5),
        "has_ex": st.session_state.user_data.get("has_exercise", False)
    }

    st.info(f"Chào {display_name}! Cập nhật trạng thái để mở khóa AI.")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        # --- CỘT 1: SINH HOẠT ---
        with col1:
            st.subheader("🌙 Giấc ngủ & 💧 Nước")
            water_liters = st.slider(
                "Lượng nước (Lít):", 0.0, 4.0, defaults["water"], 0.1)
            st.divider()
            sleep_hours = st.slider(
                "Giấc ngủ (Giờ):", 0.0, 12.0, defaults["sleep"], 0.5)

            # Logic chất lượng ngủ
            q_options = get_quality_options(sleep_hours)
            q_name = st.select_slider("Cảm giác khi dậy:", options=list(
                q_options.keys()), value=list(q_options.keys())[-1])
            q_score = q_options[q_name]

        # --- CỘT 2: VẬN ĐỘNG (NÂNG CẤP UI) ---
        with col2:
            st.subheader("🏋️ Vận động")
            has_ex = st.toggle("Hôm nay có tập luyện?",
                               value=defaults["has_ex"])

            # Biến lưu kết quả tạm
            ex_score = 0.0
            ex_detail = "Không"
            limit_stress_from_ex = 3  # Mặc định không tập thì không giảm stress trần

            if has_ex:
                # HIỆN UI CHỌN MÔN (Giống Dialog)
                act_gate = st.selectbox("Môn thể thao", list(
                    sport_config.keys()), key="gate_act")
                av_int = sport_config.get(act_gate, ["Vừa"])

                c_g1, c_g2 = st.columns(2)
                with c_g1:
                    dur_gate = st.number_input(
                        "Phút:", min_value=15, value=30, step=15, key="gate_dur")
                with c_g2:
                    int_gate = st.selectbox("Mức độ:", av_int, key="gate_int")

                # Tính điểm ngay tại đây
                ex_score = calculate_single_activity_score(int_gate)
                ex_detail = f"{act_gate} ({int_gate})"

                # Tính giới hạn stress
                if int_gate == "Cao (High Intensity)" or dur_gate >= 60:
                    limit_stress_from_ex = 0
                elif int_gate == "Vừa" or dur_gate >= 30:
                    limit_stress_from_ex = 1
                else:
                    limit_stress_from_ex = 2

            st.divider()

            # Logic Stress (Kết hợp tập luyện)
            st.write("Stress hiện tại:")
            # Tham số giả để lấy list key
            s_options = get_stress_options(has_ex, 30, "Vừa")
            s_names = list(s_options.keys())

            # Nếu tập nặng, tự động khóa các mức Stress cao
            if limit_stress_from_ex == 0:
                st.success(
                    "🔥 Bài tập cường độ cao hoặc thường xuyên đã xả sạch Stress!")
                s_name = "Thoải mái"  # Mức thấp nhất
                s_score = 0
            else:
                # Chỉ hiện các mức stress <= limit
                valid_s_names = [
                    name for name in s_names if s_options[name] <= limit_stress_from_ex]
                # Nếu list rỗng (trường hợp hiếm), lấy mức thấp nhất
                if not valid_s_names:
                    valid_s_names = [s_names[0]]

                s_name = st.select_slider(
                    "Mức độ:", options=s_names, value=valid_s_names[-1])
                # Lưu ý: Ở trên mình cho chọn full options, nhưng logic bên dưới sẽ ép xuống min
                raw_score = s_options[s_name]
                s_score = min(raw_score, limit_stress_from_ex)

                if raw_score > s_score:
                    st.caption(
                        f"✨ Stress thực tế được giảm xuống mức {s_score} nhờ tập luyện.")

        # NÚT SUBMIT
        if st.button("🚀 CẬP NHẬT VÀO HỆ THỐNG", type="primary", use_container_width=True):
            # 1. Cập nhật Dictionary hoạt động (Cho đồng bộ với Dialog)
            if has_ex:
                st.session_state.daily_activities = {
                    act_gate: {
                        "intensity": int_gate,
                        "duration": dur_gate,
                        "score": ex_score
                    }
                }
            else:
                st.session_state.daily_activities = {}

            # 2. Lưu User Data
            st.session_state.user_data = {
                "sleep_hours": sleep_hours,
                "sleep_quality": q_score,
                "water_consumed": water_liters,
                "stress_score": s_score,
                "has_exercise": has_ex,
                "exercise_score": ex_score,
                "exercise_detail": ex_detail
            }
            st.session_state.health_submitted = True
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
                    st.session_state.bio_data = user_info.get(
                        'personalization', {}).get('biometrics', {})
                    st.session_state.payment_data = user_info.get(
                        'payment_subscription', {})
                    st.session_state.sys_settings = user_info.get(
                        'general_settings', {})
                    st.rerun()
                else:
                    st.error("Sai thông tin đăng nhập!")

        with col2:
            st.markdown("### Khách truy cập")
            st.info(
                "Trải nghiệm nhanh các tính năng mà không cần lưu trữ dữ liệu lâu dài.")
            if st.button("👤 DÙNG THỬ (GUEST)", use_container_width=True):
                # 1. Gọi hàm lấy dữ liệu Guest từ User_data.py
                guest_data = get_guest_data()

                # 2. Bật trạng thái đăng nhập
                st.session_state.is_logged_in = True

                # 3. [QUAN TRỌNG] Đưa toàn bộ ví tiền và sinh trắc của Guest vào Session
                st.session_state.payment_data = guest_data.get(
                    'payment_subscription', {})
                st.session_state.account_info = guest_data.get('account', {})
                st.session_state.db_grades = guest_data.get(
                    'learning_results', {}).get('grades', [])

                # Nạp thêm sinh trắc và cài đặt (để trang Settings không bị lỗi 0.0)
                st.session_state.bio_data = guest_data.get(
                    'personalization', {}).get('biometrics', {})
                st.session_state.sys_settings = guest_data.get(
                    'general_settings', {})

                # 4. Tạo dữ liệu trạng thái hằng ngày mặc định (vì Guest thường chưa có daily_status)
                if 'daily_status' not in guest_data:
                    st.session_state.user_data = {
                        "sleep_hours": 7.0, "sleep_quality": 4,
                        "water_consumed": 0.0, "stress_score": 1,
                        "has_exercise": False, "exercise_detail": "Không"
                    }
                else:
                    st.session_state.user_data = guest_data.get(
                        'daily_status', {})

                st.rerun()


# --- LOGIC ĐIỀU KHIỂN CHÍNH (ĐÃ BỌC ĐĂNG NHẬP) ---

# 1. Khởi tạo trạng thái đăng nhập
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# 2. Kiểm tra: Chưa đăng nhập -> Hiện Login
if not st.session_state.is_logged_in:
    render_login()

# 3. Đã đăng nhập
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
            acc_info = st.session_state.get('account_info', {})
            pay_data = st.session_state.get('payment_data', {})
            username = acc_info.get('username', 'Guest')
            fair_coin = pay_data.get('fair_coin_balance', 0)
            tier = pay_data.get('current_tier', 'Standard')
            active_model = st.session_state.get(
                'active_model', 'Gemini 2.5 Flash')

            with st.popover(f"👤 {username.upper()}"):
                st.markdown(f"**Thông tin tài khoản**")
                col_coin, col_tier = st.columns(
                    [1, 1], vertical_alignment="center")
                # Tạo khung hiển thị Coin giống style st.status
                with col_coin:
                    st.image("assets/fair-coin.png", width=100,
                             caption=f"**{fair_coin}**")
                with col_tier:
                    st.markdown("# 🏅Hạng", text_alignment="center")
                    st.markdown(f"`{tier}`")

                # Hiển thị Model AI đang sử dụng (Style bạn thích)
                st.info(f"Đang kết nối: {active_model}")

                st.caption("Dữ liệu được cập nhật thời gian thực")
            # 1. LOGIC TOAST
            if 'toast_msg' in st.session_state and st.session_state.toast_msg:
                st.toast(st.session_state.toast_msg)
                st.session_state.toast_msg = None
                st.session_state.temp_water_added = 0.0
            # 2. TRẠNG THÁI SỨC KHỎE
            if st.button("❤️ Trạng thái sức khỏe", use_container_width=True):
                show_health_status_dialog()
