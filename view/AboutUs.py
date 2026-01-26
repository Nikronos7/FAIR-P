import streamlit as st


def render_about_us():
    # --- 0. CSS TÙY CHỈNH (ĐỂ BO GÓC ẢNH) ---
    # Thay vì viết style vào st.image, ta viết CSS ở đây
    st.markdown("""
        <style>
        /* Bo góc cho tất cả các ảnh trong trang này */
        img {
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. HERO SECTION ---
    st.image("https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=2000&auto=format&fit=crop",
             use_container_width=True,
             caption="The Dawn of Bio-Intelligence Learning")

    st.markdown("""
        <h1 style='text-align: center; font-size: 3em; margin-bottom: 0px;'>FAIR-P</h1>
        <h3 style='text-align: center; color: gray; font-style: italic;'>Where Biological Rhythms meet Artificial Intelligence.</h3>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 2. CÂU CHUYỆN KHỞI NGUỒN ---
    # [FIX] Thêm container bao quanh khu vực này
    with st.container(border=True):
        col_story, col_img_story = st.columns(
            [1.5, 1], vertical_alignment="center")

        with col_story:
            st.markdown("### 🧬 Khởi nguồn từ sự thấu hiểu")
            st.write("""
            Trong kỷ nguyên của AI,học sinh đang đối mặt về những vấn đề học tập như kỹ năng tự học,quản lí bản thân ,phân bổ hiệu suất,...Dự án FAIR-P sinh ra nhằm hỗ trợ học sinh kết hợp cả sức khoẻ và trí tuệ để đạt hiệu quả tốt nhất cho việc học.Đây không phải là mô hình AI mạnh mẽ,nguồn tài liệu khổng lồ,mà là mô hình Trợ lí AI hỗ trợ phát triển và quản lí bản thân.
            
            **FAIR-P** (Foundational Artificial Intelligence for Reorientaion) ra đời không phải để thay thế giáo viên. 
            Chúng tôi tạo ra một **"Người bạn đồng hành kỹ thuật số"**. 
            
            Một hệ thống biết bạn mệt trước khi bạn nhận ra. Một AI biết giảm tải bài tập khi stress của bạn tăng cao. 
            Đó là sự giao thoa giữa **Công nghệ Y sinh** và **Giáo dục**.
            """)

        with col_img_story:
            st.image("https://images.unsplash.com/photo-1531746790731-6c087fecd65a?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True)

    st.divider()

    # --- 3. CÔNG NGHỆ CỐT LÕI ---
    st.markdown("<h2 style='text-align: center;'>Hệ Sinh Thái Công Nghệ</h2>",
                unsafe_allow_html=True)
    st.caption("Sự kết hợp hoàn hảo giữa 3 trụ cột sức mạnh")

    c1, c2, c3 = st.columns(3)

    with c1:
        # [FIX] Phải dùng 'with' để nội dung chui vào hộp
        with st.container(border=True):
            st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True)
            st.markdown("#### 🧠 Adaptive AI Core")
            st.write(
                "Sử dụng Gemini Flash & Pro để tự động điều chỉnh độ khó bài tập dựa trên điểm Readiness.")

    with c2:
        with st.container(border=True):
            st.image("https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True)
            st.markdown("#### ❤️ Bio-Feedback Gate")
            st.write(
                "Cổng kiểm soát sức khỏe thu thập dữ liệu: Giấc ngủ, Nước uống, Vận động để bảo vệ người dùng.")

    with c3:
        with st.container(border=True):
            st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True)
            st.markdown("#### 📊 Performance Analytics")
            st.write(
                "Hệ thống Dashboard theo dõi tiến độ học tập và sức khoẻ với độ chính xác cao.")

    st.divider()

    # --- 4. GALLERY: TẦM NHÌN GIÁO DỤC (VISION 2030) ---
    # [FIX] Thêm container bao quanh phần Intro Vision
    with st.container(border=True):
        st.markdown("""
            <h2 style='text-align: center; margin-bottom: 0px;'>🚀 Vision 2030: The Borderless School</h2>
            <h4 style='text-align: center; color: gray;'>Trường học không biên giới – Nơi AI khai phóng tiềm năng tối đa.</h4>
        """, unsafe_allow_html=True)

        st.write("")  # Tạo khoảng trống

        # --- CÂU CHUYỆN TẦM NHÌN ---
        col_vision_txt, col_vision_img = st.columns(
            [1.2, 1], vertical_alignment="center")

        with col_vision_txt:
            st.markdown("### 🎓 Tái định nghĩa 'Trường học'")
            st.write("""
            Chúng tôi tin rằng trong một thập kỷ tới, khái niệm "trường lớp" với bốn bức tường và thời khóa biểu cứng nhắc sẽ trở nên lỗi thời. 
            
            **Học sinh tương lai sẽ không cần "đến trường" để học kiến thức, mà sẽ sử dụng các nền tảng AI cá nhân hóa như FAIR-P để phát triển.**
            
            FAIR-P không chỉ là một ứng dụng luyện thi. Chúng tôi đang xây dựng một **Hệ sinh thái Học thuật Chuyên nghiệp (Professional Academic Ecosystem)** ngay tại nhà bạn.
            
            - **Không còn lớp học một chiều:** AI sẽ thiết kế bài giảng riêng biệt dựa trên tốc độ tiếp thu và trạng thái sinh học của bạn.
            - **Không còn điểm số vô hồn:** Thành tích của bạn được đo lường bằng các Dự án thực tế (Project-based Learning) và Bộ kỹ năng thế kỷ 21 (Kỹ năng mềm + Chuyên môn).
            """)

        with col_vision_img:
            st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True, caption="Mô hình học tập phi tập trung tại nhà")

    # --- CÁC TRỤ CỘT CỦA TẦM NHÌN MỚI ---
    st.write("")
    st.markdown("#### 🏛️ Ba trụ cột của Giáo dục Tương lai tại FAIR-P")

    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        # [FIX] Dùng 'with'
        with st.container(border=True):
            st.image("https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True)
            st.markdown("**1. Học qua Dự Án (AI-Guided Projects)**")
            st.caption("Thay vì làm bài tập về nhà, bạn sẽ xây dựng một ứng dụng thực tế, viết một bài luận nghiên cứu, hoặc giải quyết một vấn đề xã hội với sự hướng dẫn từng bước của AI Mentor.")

    with col_p2:
        with st.container(border=True):
            st.image("https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True)
            st.markdown("**2. Hồ sơ Kỹ năng Số (Digital Portfolio)**")
            st.caption("FAIR-P tự động tổng hợp các dự án bạn đã làm thành một Hồ sơ năng lực chuyên nghiệp, thay thế cho bảng điểm truyền thống khi nộp đơn đại học/việc làm.")

    with col_p3:
        with st.container(border=True):
            st.image("https://images.unsplash.com/photo-1593642634402-b0eb5e2eebc9?q=80&w=1000&auto=format&fit=crop",
                     use_container_width=True)
            st.markdown("**3. Cộng đồng Học thuật Toàn cầu**")
            st.caption(
                "Kết nối với những người học cùng chí hướng trên khắp thế giới, tham gia các dự án hợp tác xuyên biên giới ngay trên nền tảng FAIR-P.")

    st.info("💡 **Kết luận:** Với FAIR-P, mỗi cá nhân là một trường đại học thu nhỏ, nơi tiềm năng được khai phóng tối đa mà không bị giới hạn bởi không gian và thời gian.")

    # --- 5. ĐỘI NGŨ SÁNG LẬP (HUMAN OS HUB) ---
    st.divider()
    st.markdown("""
        <div style="text-align: center;">
            <h4 style="color: #FF4B4B; letter-spacing: 2px; margin-bottom: 0;">POWERED BY</h4>
            <h1 style="font-size: 3.5em; margin-top: 0;">HUMAN OS HUB</h1>
            <p style="font-style: italic; color: gray;">"Optimizing the Operating System of Human Potential"</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")  # Spacer

    # --- A. LEADER PROFILE ---
    with st.container(border=True):
        col_leader_img, col_leader_bio = st.columns(
            [1, 2], vertical_alignment="center")
        with col_leader_img:
            st.image(
                "https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=160)
        with col_leader_bio:
            st.markdown("### NGUYỄN VĂN THẮNG")
            st.caption("**FOUNDER & LEAD AI ARCHITECT**")
            st.write("""
            Kiến trúc sư trưởng của FAIR-P. Người định hình tầm nhìn về sự cộng sinh giữa Con người và AI.
            
            🚀 **Khát vọng:** Đưa trí tuệ Việt vươn tầm thế giới**.
            """)

    # --- B. CORE TEAM ---
    st.write("")
    col_mem1, col_mem2, col_mem3 = st.columns(3)

    # Member 1
    with col_mem1:
        # [FIX] Dùng 'with' để nội dung chui vào hộp
        with st.container(border=True):
            st.image(
                "https://cdn-icons-png.flaticon.com/512/4140/4140037.png", width=100)
            st.markdown("**TRẦN HOÀNG NAM**")
            st.caption("💻 *FrontEnd*")
            st.write(
                "Là người tối ưu hóa giao diện và xử lý yêu cầu của người dùng. Giúp trải nghiệm người dùng được tối ưu.")

    # Member 2
    with col_mem2:
        with st.container(border=True):
            st.image(
                "https://cdn-icons-png.flaticon.com/512/4140/4140057.png", width=100)
            st.markdown("**TRẦN MINH HOÀNG**")
            st.caption("💻 *BackEnd*")
            st.write(
                "Là người xử lí dữ liệu từ người dùng để nâng cao chất lượng dữ liệu.")

    # Member 3
    with col_mem3:
        with st.container(border=True):
            st.image(
                "https://cdn-icons-png.flaticon.com/512/4140/4140061.png", width=100)
            st.markdown("**VÕ VĂN MINH QUÂN**")
            st.caption("🛡️ *Operations Manager*")
            st.write(
                "Cánh tay phải đắc lực của Leader. Quản trị vận hành và đảm bảo tiến độ dự án luôn đúng đường ray.")

    # --- 6. LỘ TRÌNH PHÁT TRIỂN (ROADMAP) ---
    st.divider()
    st.markdown("### 🗺️ Lộ Trình Phát Triển (Roadmap 2026)")

    # Dùng layout cột để tạo Timeline
    c_r1, c_r2, c_r3, c_r4 = st.columns(4)

    with c_r1:
        # [FIX] Thêm with st.container để đóng hộp nội dung
        with st.container(border=True):
            st.info("**Quý 1: Genesis (Khởi tạo)**\n\n*(Tháng 1 - 3/2026)*")
            st.write(
                "✅ **Ra mắt Demo (Completed).**\n 📚Nghiên cứu kiến trúc Database tối ưu.\n 🛠️Tinh chỉnh UX trên nền tảng Streamlit.")

    with c_r2:
        with st.container(border=True):
            st.warning(
                "**Quý 2: Optimization (Tối ưu)**\n\n*(Tháng 4 - 6/2026)*")
            st.write(
                "🛠️ Phát triển Logic thuật toán lõi.\n🛠️ Tái cấu trúc luồng dữ liệu (Data Flow).\n🛠️ Nâng cấp giao diện (UI) toàn diện.")

    with c_r3:
        with st.container(border=True):
            st.error("**Quý 3: Integration (Tích hợp)**\n\n*(Tháng 7 - 9/2026)*")
            st.write(
                "🧠 Tích hợp đa mô hình AI (Multi-Model).\n🔒 Nâng cấp lớp bảo mật dữ liệu.\n⚡ Mở rộng các tiện ích hệ thống.")

    with c_r4:
        with st.container(border=True):
            st.success(
                "**Quý 4: Ecosystem (Hệ sinh thái)**\n\n*(Tháng 10 - 12/2026)*")
            st.write(
                "📚 Tái quy hoạch kho dữ liệu học thuật.\n🌐 Nghiên cứu mô hình Mạng xã hội học tập.\n🤝 Kết nối tri thức toàn cầu.")

    # --- 7. LIÊN HỆ & ĐÁNH GIÁ (FEEDBACK) ---
    st.divider()
    st.markdown("### 💌 Liên hệ & Góp ý")

    col_contact, col_feedback = st.columns([1, 1.5])

    with col_contact:
        st.markdown("#### 🏢 HUMAN OS HUB HQ")
        st.write("📍 **Địa chỉ:** Đà Nẵng, Việt Nam")
        st.write("📧 **Email:** fairpproject@gmail.com")
        st.write("🌐 **Website:** fair-p.streamlit.app")
        st.write("📞 **Hotline:** (+84) 905 xxx xxx")

        # Các nút mạng xã hội giả lập
        st.markdown("""
            [Facebook](#) | [LinkedIn](#) | [Github](#)
        """)

    with col_feedback:
        # [FIX QUAN TRỌNG] Phải dùng 'with' để nội dung chui vào trong hộp
        with st.container(border=True):
            st.markdown("#### 🌟 Trải nghiệm của bạn thế nào?")

            # Form đánh giá
            with st.form("feedback_form"):
                user_name = st.text_input("Tên của bạn (Tùy chọn)")
                rating = st.select_slider("Mức độ hài lòng", options=[
                                          "😞", "😐", "🙂", "😀", "🤩"], value="🤩")
                feedback_text = st.text_area(
                    "Góp ý cho Human OS Hub phát triển hơn:")

                submitted = st.form_submit_button(
                    "🚀 Gửi đánh giá", use_container_width=True)

                if submitted:
                    st.balloons()
                    st.success(
                        f"Cảm ơn {user_name if user_name else 'bạn'}! Đội ngũ Human OS Hub đã ghi nhận góp ý 5 sao của bạn.")

    # ---  FOOTER NÂNG CẤP (ENTERPRISE STYLE) ---
    st.divider()

    # Khu vực Quote trung tâm (Typography đẹp)
    st.markdown("""
        <div style="text-align: center; padding: 20px 0px;">
            <h2 style="color: #5D6D7E; font-family: 'Georgia', serif; font-style: italic; font-weight: 400;">
                "Humanity as the Core, Technology as the Catalyst."
            </h2>
            <p style="color: #AEB6BF; letter-spacing: 3px; font-size: 0.8em;">— HUMAN OS HUB PHILOSOPHY —</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Footer 3 cột chuyên nghiệp
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])

    with f_col1:
        st.markdown("### **HUMAN OS HUB**")
        st.write("""
            Chúng tôi kiến tạo hệ sinh thái AI thích ứng, giúp thế hệ trẻ Việt Nam 
            tối ưu hóa hiệu suất học tập thông qua dữ liệu sinh học thực tế.
        """)
        st.caption("📍 Da Nang City, Vietnam | Global Vision")

    with f_col2:
        st.markdown("🚀 **Hệ sinh thái**")
        st.markdown("""
            - [FAIR-P Platform](#)
            - [Bio-Gate System](#)
            - [AI Mentorship](#)
            - [Skill Portfolio](#)
        """)

    with f_col3:
        st.markdown("🛡️ **Cam kết**")
        st.markdown("""
            - [Bảo mật dữ liệu](#)
            - [Điều khoản dịch vụ](#)
            - [Chính sách AI](#)
            - [Hỗ trợ 24/7](#)
        """)

    # Dòng cuối cùng
    st.write("")
    st.markdown("---")

    # Social Media & Copyright
    bottom_col1, bottom_col2 = st.columns([1, 1])
    with bottom_col1:
        st.caption("© 2026 **Human OS Hub**. All Rights Reserved.",)
        st.markdown("""
            <div style="font-size: 1em; color: #AEB6BF; margin-top: -10px;">
                Visuals sourced from: <a href="https://unsplash.com" target="_blank" style="color: #AEB6BF; text-decoration: none;">Unsplash</a> & 
                <a href="https://www.flaticon.com" target="_blank" style="color: #AEB6BF; text-decoration: none;">Flaticon</a>
            </div>
        """, unsafe_allow_html=True)
    with bottom_col2:
        st.markdown("""
            <div style="text-align: right; color: gray; font-size: 0.8em;">
                FB • LN • GH • TW
            </div>
        """, unsafe_allow_html=True)


# Gọi hàm render để test trực tiếp nếu chạy file này
if __name__ == "__main__":
    render_about_us()
