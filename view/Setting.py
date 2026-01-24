import streamlit as st
import time


@st.dialog("🚀 NÂNG CẤP THÀNH CÔNG")
def show_upgrade_success(plan_name):
    # Lấy tên người dùng
    username = st.session_state.get('account_info', {}).get('username', 'Bạn')

    # Hiệu ứng dựa trên gói cước
    if "Legend" in plan_name:
        st.snow()  # Tuyết rơi cho Legend
        st.header(f"👑 CHÀO MỪNG LEGEND: {username.upper()}")
        st.write("Bạn đã sở hữu đặc quyền cao nhất của hệ thống FAIR-P.")
    elif "Artisan" in plan_name:
        st.balloons()  # Bóng bay cho Artisan
        st.header(f"✨ CHÚC MỪNG ARTISAN: {username.upper()}")
        st.write("Bạn đã mở khóa lộ trình học tập tối ưu cùng Agentic AI.")

    st.divider()
    st.write(
        "Cảm ơn bạn đã tin dùng FAIR-P. Hãy bắt đầu hành trình chinh phục mục tiêu ngay bây giờ!")

    if st.button("Trải nghiệm ngay 🚀", use_container_width=True):
        st.rerun()


@st.dialog("📺 HỆ THỐNG PHÁT QUẢNG CÁO")
def show_ad_dialog():
    st.write("Đang tải tài trợ... Vui lòng đợi trong giây lát.")

    # 1. Thanh tiến trình chạy tự động
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.03)  # Tổng cộng khoảng 3 giây
        progress_bar.progress(i + 1)

    # 2. XỬ LÝ TỰ ĐỘNG NGAY SAU KHI XEM XONG
    # Cộng tiền trực tiếp
    st.session_state.payment_data['fair_coin_balance'] += 100

    # Gửi một thông báo nhỏ (Toast) để người dùng biết tiền đã vào túi
    st.session_state.toast_msg = "100 Fair Coin đã được cộng vào ví của bạn!"

    # 3. Lệnh đóng hộp thoại và cập nhật Sidebar ngay lập tức
    st.rerun()


@st.dialog("🚀 KÍCH HOẠT TRÍ TUỆ MỚI")
def show_model_success(model_name):
    """
    Hàm hiển thị thông báo khi người dùng nâng cấp bộ não AI thành công.
    """
    # Lấy tên người dùng để cá nhân hóa lời chào
    username = st.session_state.get('account_info', {}).get('username', 'Bạn')

    # Hiệu ứng và nội dung dựa trên Model bạn chỉ định
    if "Latest" in model_name or "VIP" in model_name:
        st.header(f"👑 ĐỈNH CAO TRÍ TUỆ: {username.upper()}")
        st.success(f"### {model_name}")
        st.write(
            "Hệ thống FAIR-P đã đồng bộ hoàn toàn với Model mạnh mẽ nhất năm 2026.")

    elif "3.0" in model_name:
        st.header(f"✨ NÂNG CẤP THÀNH CÔNG: {username.upper()}")
        st.info(f"### {model_name}")
        st.write(
            "Trợ lý của bạn đã thông minh hơn với khả năng suy luận logic chuyên sâu.")

    st.divider()
    st.write("🌟 **Cải tiến:** Tốc độ xử lý nhanh hơn, hỗ trợ giải các bài tập phức tạp và đưa ra lời khuyên học tập tối ưu nhất.")

    if st.button("Trải nghiệm ngay 🚀", use_container_width=True):
        st.rerun()


def render_settings():
    # 1. Kiểm tra đăng nhập
    if 'account_info' not in st.session_state:
        st.warning("⚠️ Vui lòng đăng nhập để truy cập cài đặt!")
        st.stop()

    acc_info = st.session_state.get('account_info', {})

    st.title("⚙️ CÀI ĐẶT HỆ THỐNG")

    # TẠO CÁC TAB
    tab_profile, tab_wallet, tab_system = st.tabs([
        "👤 Hồ sơ & Sinh trắc",
        "💳 Ví & Gói cước",
        "🖥️ Hệ thống"
    ])

    # --- TAB 1: HỒ SƠ & SINH TRẮC (CÓ NÚT ĐĂNG XUẤT) ---
    with tab_profile:
        st.info("Các tính năng này đang được phát triển!")
        col_info, col_bio = st.columns(2)

        with col_info:
            st.subheader("Thông tin cơ bản")
            with st.container(border=True):
                st.text_input("Tên đăng nhập", value=acc_info.get(
                    'username'), disabled=True)
                st.text_input("Email liên kết", value=acc_info.get(
                    'gmail'), disabled=True)
                st.button("Đổi mật khẩu", use_container_width=True)

        with col_bio:
            st.subheader("Chỉ số cơ thể")
            bio = st.session_state.get('bio_data', {})
            with st.container(border=True):
                c1, c2 = st.columns(2)
                weight = c1.number_input(
                    "Cân nặng (kg)", value=float(bio.get('weight_kg', 60)))
                height = c2.number_input(
                    "Chiều cao (cm)", value=float(bio.get('height_cm', 170)))
                if height > 0:
                    bmi = weight / ((height / 100) ** 2)

                    # Phân loại và đưa ra lời khuyên
                    if bmi < 18.5:
                        status = "Gầy"
                        color = "blue"
                        advice = "Nên tập trung vào các bài tập kháng lực (Calisthenics nhẹ) và tăng cường dinh dưỡng."
                    elif 18.5 <= bmi < 24.9:
                        status = "Bình thường"
                        color = "green"
                        advice = "Tuyệt vời! Hãy duy trì Tempo Run 2-3 buổi/tuần và Calisthenics để giữ cơ thể săn chắc."
                    elif 25 <= bmi < 29.9:
                        status = "Thừa cân"
                        color = "orange"
                        advice = "Nên tăng cường các bài tập Cardio như chạy bộ hoặc nhảy dây để đốt cháy calo dư thừa."
                    else:
                        status = "Béo phì"
                        color = "red"
                        advice = "Cần ưu tiên đi bộ nhanh và kiểm soát chế độ ăn uống nghiêm ngặt trước khi tập nặng."

                    # Hiển thị kết quả
                    st.markdown(
                        f"Chỉ số BMI của bạn: **{bmi:.1f}** (<span style='color:{color}'>{status}</span>)", unsafe_allow_html=True)
                    st.info(f"💡 **Lời khuyên:** {advice}")

        st.divider()
        # --- KHU VỰC ĐĂNG XUẤT NẰM Ở ĐÂY ---
        st.markdown("### Quản lý phiên làm việc")
        col_logout, col_empty = st.columns([1, 2])
        with col_logout:
            if st.button("🚪 ĐĂNG XUẤT", type="primary", use_container_width=True):
                # Xóa toàn bộ session và quay về màn hình login
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    # --- TAB 2: VÍ & GÓI CƯỚC ---
    with tab_wallet:
        pay_data = st.session_state.get('payment_data', {})
        current_vnd = pay_data.get('vnd_balance', 0)
        current_coin = pay_data.get('fair_coin_balance', 0)
        current_tier = pay_data.get('current_tier', 'Standard Member')

        # 1. ĐỊNH NGHĨA THỨ HẠNG (Hệ thống xương sống của FAIR-P)
        TIER_RANK = {
            "Standard Member": 0,
            "Artisan (Premium)": 1,
            "Legend (Elite)": 2
        }

        # Đồng bộ hóa Model Rank theo Gói cước
        user_tier_rank = TIER_RANK.get(current_tier, 0)

        # Khởi tạo rank model đã mua nếu chưa có
        if 'bought_model_rank' not in st.session_state:
            st.session_state.bought_model_rank = 0

        # Logic: Lấy mức độ thông minh cao nhất mà người dùng đang có
        effective_model_rank = max(
            user_tier_rank, st.session_state.bought_model_rank)

        # 2. Hiển thị số dư hiện tại
        st.subheader("💰 Tài chính của bạn")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Số dư VND", f"{current_vnd:,} đ")
        with c2:
            st.metric("Fair Coin", f"{current_coin}")
            if st.button("📺 XEM QUẢNG CÁO (+100)", use_container_width=True, type="primary"):
                show_ad_dialog()
        with c3:
            st.info(f"Hạng: **{current_tier}**")

        st.divider()

        # 3. Giao diện Model AI
        st.subheader("🤖 Nâng cấp Trí tuệ AI")
        st.caption(
            "Model cao cấp giúp AI suy luận logic và giải bài tập hiệu quả hơn")

        m1, m2, m3 = st.columns(3)
        PRICE_3_0_FLASH = 500
        PRICE_LATEST_VIP = 1500

        # --- MODEL 1: GEMINI 2.5 FLASH (Mặc định) ---
        with m1:
            with st.container(border=True):
                st.markdown("### Gemini 2.5 Flash")
                st.markdown("## MIỄN PHÍ")
                st.divider()
                st.write("⚡ Tốc độ cực nhanh")
                st.button("Đã sở hữu", disabled=True,
                          use_container_width=True, key="m_flash")

        # --- MODEL 2: GEMINI 3.0 FLASH (Rank 1) ---
        with m2:
            with st.container(border=True):
                st.markdown("### Gemini 3.0 Flash")
                st.markdown(f"## 🪙 {PRICE_3_0_FLASH}")
                st.divider()
                st.write("🧠 Suy luận chuyên sâu")

                if effective_model_rank >= 1:
                    status = "Mặc định (Artisan/Legend)" if user_tier_rank >= 1 else "Đã sở hữu"
                    st.button(status, disabled=True,
                              use_container_width=True, key="m_30_owned")
                else:
                    if current_coin >= PRICE_3_0_FLASH:
                        if st.button("Kích hoạt ngay", use_container_width=True, key="m_30_buy"):
                            st.session_state.payment_data['fair_coin_balance'] -= PRICE_3_0_FLASH
                            st.session_state.bought_model_rank = 1
                            st.session_state.active_model = "Gemini 3.0 Flash"
                            show_model_success("3.0")
                    else:
                        st.button(f"Thiếu {PRICE_3_0_FLASH - current_coin} 🪙",
                                  disabled=True, use_container_width=True)

        # --- MODEL 3: GEMINI LATEST (Rank 2) ---
        with m3:
            with st.container(border=True):
                st.markdown("### Gemini Latest (VIP)")
                st.markdown(f"## 🪙 {PRICE_LATEST_VIP}")
                st.divider()
                st.write("🎨 Sáng tạo & Coding")

                if effective_model_rank >= 2:
                    status = "Mặc định (Legend)" if user_tier_rank >= 2 else "Đã sở hữu"
                    st.button(status, disabled=True,
                              use_container_width=True, key="m_latest_owned")
                else:
                    if current_coin >= PRICE_LATEST_VIP:
                        if st.button("Kích hoạt ngay", use_container_width=True, key="m_latest_buy"):
                            st.session_state.payment_data['fair_coin_balance'] -= PRICE_LATEST_VIP
                            st.session_state.bought_model_rank = 2
                            st.session_state.active_model = "Gemini Flash Latest"
                            show_model_success("Latest")
                    else:
                        st.button(f"Thiếu {PRICE_LATEST_VIP - current_coin} 🪙",
                                  disabled=True, use_container_width=True)

        st.divider()
        # 3. Danh sách gói cước (Logic nâng cấp & Hiệu ứng)
        st.subheader("💎 Nâng cấp gói cước")
        p1, p2, p3 = st.columns(3)

        # Thứ hạng để chống hạ cấp
        TIER_RANK = {
            "Standard Member": 0,
            "Artisan (Premium)": 1,
            "Legend (Elite)": 2
        }

        current_rank = TIER_RANK.get(pay_data.get('current_tier'), 0)
        PRICE_ARTISAN = 150000
        PRICE_LEGEND = 2000000

        # --- CỘT 1: STANDARD ---
        with p1:
            with st.container(border=True):
                st.markdown("### Standard")
                st.markdown("## Miễn phí")
                st.divider()
                st.write("✅ Lời khuyên cơ bản")
                st.button("Đã sở hữu", disabled=True,
                          use_container_width=True, key="std_btn")

        # --- CỘT 2: ARTISAN ---
        with p2:
            with st.container(border=True):
                st.markdown("### Artisan")
                st.markdown(f"## {PRICE_ARTISAN:,}đ/tháng")
                st.divider()
                st.write("✅ AI hỗ trợ chuyên sâu")
                st.write("✅ Phân tích sức khoẻ")
                st.write("✅ Phân tích lộ trình và tối ưu học tập")

                if current_rank >= 1:
                    status_label = "Gói hiện tại" if current_rank == 1 else "Đã sở hữu"
                    st.button(status_label, disabled=True,
                              use_container_width=True, key="art_owned")
                else:
                    if st.button("Nâng cấp", use_container_width=True, key="art_up"):
                        if current_vnd >= PRICE_ARTISAN:
                            st.session_state.payment_data['vnd_balance'] -= PRICE_ARTISAN
                            st.session_state.payment_data['current_tier'] = "Artisan (Premium)"
                            show_upgrade_success("Artisan (Premium)")
                        else:
                            st.error(
                                f"❌ Thiếu {PRICE_ARTISAN - current_vnd:,}đ")

        # --- CỘT 3: LEGEND ---
        with p3:
            with st.container(border=True):
                st.markdown("### Legend")
                st.markdown(f"## {PRICE_LEGEND:,}đ/tháng")
                st.divider()
                st.write("✅ Ai Gemini Pro")
                st.write("✅ Tác nhân AI")
                st.write("✅ Tự động hoá các dịch vụ")
                st.write("✅ Nâng cao hiệu suất thực tế")
                st.write("✅ Tất cả tính năng của Artisan")

                if current_rank >= 2:
                    st.button("Gói hiện tại", disabled=True,
                              use_container_width=True, key="leg_owned")
                else:
                    if st.button("Mua ngay", use_container_width=True, key="leg_up"):
                        if current_vnd >= PRICE_LEGEND:
                            st.session_state.payment_data['vnd_balance'] -= PRICE_LEGEND
                            st.session_state.payment_data['current_tier'] = "Legend (Elite)"
                            show_upgrade_success("Legend (Elite)")
                        else:
                            st.error(
                                f"❌ Thiếu {PRICE_LEGEND - current_vnd:,}đ")

    # --- TAB 3: HỆ THỐNG ---
    with tab_system:
        st.info("Các tính năng này đang được phát triển!")
        st.subheader("Tùy chỉnh giao diện")
        settings = st.session_state.get('sys_settings', {})
        st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"], index=0)
        st.toggle("Chế độ tối (Dark Mode)", value=(
            settings.get('theme') == "Dark Mode"))


render_settings()
