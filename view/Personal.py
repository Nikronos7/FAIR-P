import streamlit as st
import plotly.graph_objects as go
import datetime
import pandas as pd

# --- IMPORT LOGIC ---
# 1. Chatbot: Để nói chuyện với Gemini
from logic.chatbot import chat_logic
# 2. Calculations: Để tính điểm sức khỏe
from logic.calculations import calculate_readiness, get_ai_mode, get_progress_data
# 3. Prompts: Điều chỉnh logic theo sức khoẻ
from logic.prompts import get_system_prompt

# --- HÀM VẼ RADAR CHART ---


def plot_radar_chart(data):
    # 1. Chuẩn hóa dữ liệu về thang 10
    score_sleep = min((data['sleep_hours'] / 8) * 10, 10)
    score_water = min((data['water_consumed'] / 2.5) * 10, 10)
    score_ex = data.get('exercise_score', 0) * 5  # 2.0 -> 10 điểm
    score_mind = (3 - data['stress_score']) / 3 * 10

    categories = ['Giấc ngủ', 'Nước uống', 'Vận động', 'Tinh thần (Stress)']

    fig = go.Figure()

    # Lớp 1: Mục tiêu
    fig.add_trace(go.Scatterpolar(
        r=[8, 8, 8, 8],
        theta=categories,
        fill='toself',
        name='Mục tiêu cân bằng',
        line_color='lightgray',
        opacity=0.4
    ))

    # Lớp 2: Hiện trạng
    fig.add_trace(go.Scatterpolar(
        r=[score_sleep, score_water, score_ex, score_mind],
        theta=categories,
        fill='toself',
        name='Hiện trạng',
        line_color='#00CC96'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        height=350,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig


# --- TÍNH TOÁN TOÀN CỤC ---
if 'user_data' in st.session_state:
    data = st.session_state.user_data
    readiness = calculate_readiness(data)
    ai_mode_name, status_type, active_model_id = get_ai_mode(readiness)
else:
    st.warning("⚠️ Vui lòng cập nhật thông tin sức khỏe ở Sidebar!")
    st.stop()

# 1. SIDEBAR
with st.sidebar:
    selected = st.radio(
        "Điều hướng:",
        ["Học tập", "Dashboard", "Tiến trình"],
        index=1  # Mặc định vào Dashboard
    )
# 2. NỘI DUNG TỪNG TRANG

# ==================================================
# TRANG 1: HỌC TẬP (CHAT VỚI AI)
# ==================================================
if selected == "Học tập":
    # Khởi tạo lịch sử chat nếu chưa có
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- 1. TÍNH TOÁN TRẠNG THÁI (SỨC KHỎE & MODEL) ---
    user_data = st.session_state.get('user_data', {})
    readiness_score = calculate_readiness(user_data)

    # Tự động lấy Model xịn nhất và Persona theo Rank
    ai_name, ai_color, active_model_id = get_ai_mode(readiness_score)
    st.session_state.active_model = ai_name

    # --- 2. LẤY DỮ LIỆU TỪ GIỎ HÀNG KIẾN THỨC ---
    # Đây là bước quan trọng để kết nối với trang Skills.py
    active_skills_cart = st.session_state.get('active_skills', [])

    # Hiển thị thông báo nhỏ nếu đang có kỹ năng được nạp (UX)
    if active_skills_cart:
        skill_titles = ", ".join([s['title'] for s in active_skills_cart])
        st.caption(f"⚡ **AI đang được nạp kiến thức:** {skill_titles}")

    # --- 3. GIAO DIỆN CHAT ---
    chat_container = st.container(height=450, border=True)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # --- 4. XỬ LÝ INPUT & PROMPT ENGINEERING ---
    if prompt := st.chat_input(f"Hỏi {ai_name}..."):
        # A. Hiển thị tin nhắn người dùng
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            # B. Xử lý phía AI
            with st.chat_message("assistant"):
                # Tạo hiệu ứng "đang suy nghĩ" chuyên nghiệp
                with st.status(f"🚀 {ai_name} đang phân tích...", state="running", expanded=False) as status:
                    st.write(f"🧠 **Model:** `{active_model_id}`")
                    st.write(f"❤️ **Sức khỏe User:** {readiness_score}/100")

                    if active_skills_cart:
                        st.write(
                            f"📚 **Kỹ năng vận dụng:** {len(active_skills_cart)} module")

                    # [LOGIC CỐT LÕI] Tạo System Prompt
                    # Lấy tên user
                    acc_info = st.session_state.get('account_info', {})
                    user_name = acc_info.get('username', 'Bạn')

                    # Gọi hàm get_system_prompt với đầy đủ 4 tham số
                    system_instruction = get_system_prompt(
                        readiness_score=readiness_score,
                        model_id=active_model_id,
                        username=user_name,
                        active_skills=active_skills_cart  # <--- QUAN TRỌNG: Truyền giỏ hàng vào đây
                    )

                    # Ghép kịch bản vào câu hỏi
                    full_prompt_to_ai = f"{system_instruction}\n\n---\nUser Input: {prompt}"

                    st.write("✅ Đã xây dựng xong ngữ cảnh.")

                    # Gọi API lấy câu trả lời
                    response = chat_logic.get_response(
                        full_prompt_to_ai, model_id=active_model_id)

                    status.update(
                        label=f"✅ {ai_name} đã trả lời", state="complete")

                # C. Hiển thị câu trả lời của AI
                st.markdown(response)

        # D. Lưu tin nhắn Bot vào session
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
# ==================================================
# TRANG 2: DASHBOARD (BIỂU ĐỒ & SỨC KHỎE)
# ==================================================
elif selected == "Dashboard":

    # 1. Kiểm tra dữ liệu
    if 'user_data' not in st.session_state:
        st.warning("⚠️ Chưa có dữ liệu. Vui lòng cập nhật thông tin ở Sidebar!")
        st.stop()

    data = st.session_state.user_data

    # 2. HEADER: LỜI CHÀO & ĐIỂM SỐ
    head_col1, head_col2 = st.columns([2, 1])

    with head_col1:
        # --- LOGIC THỜI GIAN (Dùng thư viện datetime) ---
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 11:
            greeting = "Chào buổi sáng"
        elif 11 <= current_hour < 14:
            greeting = "Chào buổi trưa"
        elif 14 <= current_hour < 18:
            greeting = "Chào buổi chiều"
        else:
            greeting = "Chào buổi tối"

        # --- LOGIC LẤY TÊN (Lấy từ session state bên fair-p.py) ---
        # Lấy từ account_info nếu có, nếu không thì mặc định là 'Bạn'
        acc_info = st.session_state.get('account_info', {})
        display_name = acc_info.get('username', 'Nikronos7')

        # --- HIỂN THỊ ---
        st.markdown(f"### {greeting}, {display_name}! 👋")
        st.info(f"Trạng thái: {ai_mode_name}")
    with head_col2:
        st.metric("Readiness", f"{readiness}%")
        st.progress(readiness/100)

    st.divider()

    # 3. BIỂU ĐỒ RADAR & CHI TIẾT
    col_chart, col_info = st.columns([1.5, 1])

    with col_chart:
        st.markdown("##### 🕸️ Mạng lưới cân bằng")
        fig = plot_radar_chart(data)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={'staticPlot': True,
                    'displayModeBar': False, 'showTips': False}
        )

    with col_info:
        st.markdown("##### 📌 Chi tiết chỉ số")
        with st.container(border=True):
            st.metric("Giấc ngủ", f"{data['sleep_hours']}h",
                      delta=f"{data['sleep_hours'] - 8}h")

            target_water = 2.5
            st.metric("Lượng nước", f"{data['water_consumed']}L",
                      delta=f"{(data['water_consumed'] - target_water):.1f}L")

            stress_lv = ["Không có", "Thấp", "Khá",
                         "Cao"][data.get('stress_score', 0)]
            st.metric("Stress", stress_lv, delta=-
                      data.get('stress_score', 0), delta_color="inverse")

            ex_score = data.get('exercise_score', 0)
            st.metric("Vận động", f"{ex_score}/2.0 đ")

    st.info("💡 **Mẹo:** Cập nhật các chỉ số ở Sidebar bên trái để thấy biểu đồ thay đổi theo thời gian thực!")
    st.divider()
    st.subheader("🎓 Bảng Điểm Chi Tiết Học Kỳ")

    # --- BƯỚC 1: KHỞI TẠO DỮ LIỆU ---
    # Logic: Nếu chưa có bảng HOẶC bảng đang bị lỗi toàn số 0 -> Nạp lại ngay
    need_reload = 'grade_data' not in st.session_state
    if not need_reload:
        current_df = st.session_state.grade_data
        if 'Trung bình' in current_df.columns and current_df['Trung bình'].sum() == 0:
            need_reload = True

    if need_reload:
        # [FIX QUAN TRỌNG] Lấy từ db_grades (do fair-p.py nạp vào)
        raw_grades = st.session_state.get('db_grades', [])

        if raw_grades:
            data_list = []
            for i, item in enumerate(raw_grades):
                scores = [item['tx1'], item['tx2'], item['tx3'],
                          item['tx4'], item['midterm'], item['final']]
                valid_scores = [s for s in scores if s > 0]
                avg = sum(valid_scores) / \
                    len(valid_scores) if valid_scores else 0.0

                data_list.append({
                    "STT": i + 1,
                    "Môn học": item["subject"],
                    "TX 1": item["tx1"], "TX 2": item["tx2"],
                    "TX 3": item["tx3"], "TX 4": item["tx4"],
                    "Giữa kì": item["midterm"], "Cuối kì": item["final"],
                    "Trung bình": avg
                })
            df_grades = pd.DataFrame(data_list)
        else:
            # Tạo bảng rỗng nếu không có dữ liệu
            subjects = ["Toán học", "Ngữ văn", "Tiếng Anh",
                        "Vật lý", "Hóa học", "Tin học"]
            df_grades = pd.DataFrame({
                "STT": range(1, len(subjects) + 1),
                "Môn học": subjects,
                "TX 1": [0.0]*6, "TX 2": [0.0]*6, "TX 3": [0.0]*6, "TX 4": [0.0]*6,
                "Giữa kì": [0.0]*6, "Cuối kì": [0.0]*6, "Trung bình": [0.0]*6
            })

        st.session_state.grade_data = df_grades

    # --- BƯỚC 2: CẤU HÌNH & HIỂN THỊ ---
    st.session_state.grade_data = st.session_state.grade_data.sort_values(
        "STT")
    score_config = st.column_config.NumberColumn(
        min_value=0.0, max_value=10.0, step=0.1, format="%.2f", width="small")

    edited_df = st.data_editor(
        st.session_state.grade_data,
        column_config={
            "STT": st.column_config.NumberColumn(width="small", disabled=True),
            "Môn học": st.column_config.TextColumn(width="medium", disabled=True),
            "TX 1": score_config, "TX 2": score_config, "TX 3": score_config, "TX 4": score_config,
            "Giữa kì": score_config, "Cuối kì": score_config,
            "Trung bình": st.column_config.NumberColumn(format="%.2f", disabled=True, width="small")
        },
        hide_index=True,
        use_container_width=True,
        key="grade_editor_final"
    )

    # --- BƯỚC 3: XỬ LÝ SỬA ĐỔI (SYNC) ---
    if not edited_df.equals(st.session_state.grade_data):
        for index, row in edited_df.iterrows():
            all_scores = [row["TX 1"], row["TX 2"], row["TX 3"],
                          row["TX 4"], row["Giữa kì"], row["Cuối kì"]]
            valid_scores = [s for s in all_scores if s > 0]
            new_avg = sum(valid_scores) / \
                len(valid_scores) if valid_scores else 0.0
            edited_df.at[index, "Trung bình"] = new_avg

        st.session_state.grade_data = edited_df
        st.rerun()

    # --- BƯỚC 4: METRIC TỔNG ---
    avg_series = st.session_state.grade_data[st.session_state.grade_data["Trung bình"] > 0]["Trung bình"]
    final_gpa = avg_series.mean() if not avg_series.empty else 0.0
    st.metric("Điểm trung bình học kỳ (Dự kiến)", f"{final_gpa:.2f}")

# ==================================================
# TRANG 3: TIẾN TRÌNH
# ==================================================
elif selected == "Tiến trình":
    st.header("📈 Lộ Trình Phát Triển Cá Nhân")

    # Lấy dữ liệu từ file CSV
    history_df = get_progress_data()

    if history_df is None:
        # Nếu chưa có file, dùng dữ liệu giả lập để demo
        history_df = pd.DataFrame({
            "Ngày": ["18/01", "19/01", "20/01", "21/01"],
            "Readiness": [70, 85, 60, readiness]
        })

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Biểu đồ Năng lượng")
        # Sử dụng Plotly cho biểu đồ đường để đồng bộ với Radar Chart
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=history_df['Ngày'], y=history_df['Readiness'], mode='lines+markers', line_color='#00CC96'))
        fig_line.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.subheader("🏆 Thành tích")
        st.success("🔥 5 ngày học tập liên tiếp")
        st.info(f"💧 Nước đạt: {data['water_consumed']}L")

    st.divider()
    st.subheader("🎯 Mục tiêu dài hạn")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.write("**IELTS Target: 7.5**")
        st.progress(0.7, text="70% hoàn thành")
    with t2:
        st.write("**SAT Target: 1500+**")
        st.progress(0.4, text="Giai đoạn chuẩn bị")
    with t3:
        st.write("**AP Calculus BC Target: 4+/5**")
        st.progress(0.1, text="Giai đoạn làm quen")
