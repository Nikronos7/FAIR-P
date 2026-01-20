import streamlit as st
import plotly.graph_objects as go
import datetime

# --- IMPORT LOGIC ---
# 1. Chatbot: Để nói chuyện với Gemini
from logic.chatbot import chat_logic
# 2. Calculations: Để tính điểm sức khỏe
from logic.calculations import calculate_readiness, get_ai_mode

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

    # Khởi tạo lịch sử chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị tin nhắn cũ
    chat_container = st.container(height=450, border=True)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Xử lý nhập liệu mới
    if prompt := st.chat_input("Hỏi AI về bài học..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Lấy model dựa trên sức khỏe hiện tại
        # Nếu chưa có dữ liệu sức khỏe, mặc định dùng Flash
        if 'user_data' in st.session_state:
            r_score = calculate_readiness(st.session_state.user_data)
            _, _, active_model_id = get_ai_mode(r_score)
        else:
            active_model_id = "models/gemini-2.5-flash"

        with chat_container:
            with st.chat_message("assistant"):
                # Hiển thị model đang dùng để bạn biết
                st.caption(f"🚀 Đang sử dụng: {active_model_id}")

                with st.spinner("AI đang suy nghĩ..."):
                    # --- TRUYỀN MODEL ID VÀO ĐÂY ---
                    response = chat_logic.get_response(
                        prompt, model_id=active_model_id)
                    st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response})
# ==================================================
# TRANG 2: DASHBOARD (BIỂU ĐỒ & SỨC KHỎE)
# ==================================================
elif selected == "Dashboard":

    # Kiểm tra dữ liệu
    if 'user_data' not in st.session_state:
        st.warning("⚠️ Chưa có dữ liệu. Vui lòng cập nhật thông tin ở Sidebar!")
        st.stop()

    data = st.session_state.user_data

    # 1. TÍNH TOÁN ĐIỂM SỐ
    readiness = calculate_readiness(data)
    ai_mode_name, status_type, current_model_id = get_ai_mode(readiness)

    # 2. HEADER: LỜI CHÀO & ĐIỂM SỐ
    head_col1, head_col2 = st.columns([2, 1])

    with head_col1:
        current_hour = datetime.datetime.now().hour
        greeting = "Chào buổi sáng" if 5 <= current_hour < 12 else "Chào buổi chiều" if 12 <= current_hour < 18 else "Chào buổi tối"

        st.markdown(f"### {greeting}, Nikronos7! 👋")

        if status_type == "success":
            st.success(
                f"🚀 **Sẵn sàng cao độ ({readiness}/100)**: Cơ thể bạn đang ở trạng thái tốt nhất!")
        elif status_type == "info":
            st.info(
                f"⚖️ **Ổn định ({readiness}/100)**: Trạng thái cân bằng, phù hợp để ôn tập.")
        else:
            st.warning(
                f"🔋 **Cần nạp năng lượng ({readiness}/100)**: Hãy nghỉ ngơi chút nhé.")

    with head_col2:
        st.metric("Năng lượng học tập",
                  f"{readiness}/100", delta=f"AI: {ai_mode_name}")
        st.progress(readiness / 100)

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

    st.divider()
    st.info("💡 **Mẹo:** Cập nhật các chỉ số ở Sidebar bên trái để thấy biểu đồ thay đổi theo thời gian thực!")

# ==================================================
# TRANG 3: TIẾN TRÌNH
# ==================================================
elif selected == "Tiến trình":
    st.subheader("📈 Theo dõi lộ trình")
    st.progress(60)
    st.write("Tính năng đang phát triển...")
