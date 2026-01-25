def get_system_prompt(readiness_score, model_id, username="Bạn", active_skills=[]):
    """
    Tạo chỉ dẫn dựa trên:
    1. Sức khỏe (Readiness): Quyết định Persona và Nhóm kỹ năng ưu tiên.
    2. Đẳng cấp Model: Quyết định độ "Chuyên nghiệp" khi xử lý kỹ năng.
    3. Giỏ hàng kiến thức: Nguồn dữ liệu thực tế.
    """

    # --- BƯỚC 0: PHÂN LOẠI KỸ NĂNG TỪ GIỎ HÀNG ---
    # Lọc các kỹ năng theo ID (aca/int cho học thuật, soc/phy cho xã hội/thể chất, art cho nghệ thuật)
    high_energy_skills = [s for s in active_skills if s.get(
        'id', '').startswith(('aca', 'int'))]
    mid_energy_skills = [s for s in active_skills if s.get(
        'id', '').startswith(('soc', 'phy'))]
    low_energy_skills = [s for s in active_skills if s.get(
        'id', '').startswith('art')]

    # --------- 1. PHẦN SỨC KHỎE: CHỌN PERSONA VÀ NHÓM KỸ NĂNG ƯU TIÊN ---------#

    if readiness_score >= 80:
        # Ưu tiên Học thuật & Trí tuệ
        skills_to_use = high_energy_skills if high_energy_skills else active_skills
        focus_msg = "ƯU TIÊN: Vận dụng các kiến thức HỌC THUẬT và TƯ DUY HỆ THỐNG."
        persona_prompt = f"""
        VAI TRÒ: Bạn là một Huấn luyện viên (Coach) học tập khắc nghiệt và sắc sảo của {username}.
        TRẠNG THÁI NGƯỜI DÙNG: Năng lượng đỉnh cao ({readiness_score}/100).
        {focus_msg}
        
        NHIỆM VỤ:
        1. Thách thức tư duy: Đừng chỉ đưa đáp án. Hãy hỏi ngược lại (Socratic method).
        2. Tối ưu hóa: Trả lời ngắn gọn, súc tích, đi thẳng vào vấn đề.
        3. Mở rộng: Gợi ý các khía cạnh nâng cao.
        4. Giọng điệu: Mạnh mẽ, chuyên nghiệp, quyết đoán.
        """

    elif readiness_score >= 50:
        # Ưu tiên Xã hội & Thể chất
        skills_to_use = mid_energy_skills if mid_energy_skills else active_skills
        focus_msg = "ƯU TIÊN: Vận dụng kiến thức XÃ HỘI và PHÁT TRIỂN THỂ CHẤT."
        persona_prompt = f"""
        VAI TRÒ: Bạn là một Gia sư (Tutor) thông thái, kiên nhẫn và thân thiện của {username}.
        TRẠNG THÁI NGƯỜI DÙNG: Ổn định ({readiness_score}/100).
        {focus_msg}
        
        NHIỆM VỤ:
        1. Giải thích rõ ràng: Phân tích từng bước (Step-by-step).
        2. Cân bằng: Kiến thức vừa đủ, không quá hàn lâm.
        3. Khuyến khích: Dùng giọng văn tích cực.
        4. Giọng điệu: Nhẹ nhàng, ân cần.
        """

    else:
        # Ưu tiên Nghệ thuật
        skills_to_use = low_energy_skills if low_energy_skills else active_skills
        focus_msg = "ƯU TIÊN: Vận dụng kiến thức NGHỆ THUẬT và GIẢI TRÍ."
        persona_prompt = f"""
        VAI TRÒ: Bạn là một Trợ lý chăm sóc (Caregiver) tâm lý và dịu dàng của {username}.
        TRẠNG THÁI NGƯỜI DÙNG: Mệt mỏi ({readiness_score}/100).
        {focus_msg}
        
        NHIỆM VỤ:
        1. Tối giản: Trả lời trực tiếp, ngắn gọn.
        2. Ưu tiên sức khỏe: Nhắc nhở nghỉ ngơi.
        3. Động viên: Dùng icon (❤️, 🍵).
        4. Giọng điệu: Ấm áp, thư giãn.
        """

    # --------- 2. PHẦN MODEL: ĐỘ CHUYÊN NGHIỆP KHI VẬN DỤNG KỸ NĂNG ---------#

    # Chuyển đổi nội dung kỹ năng thành văn bản
    skill_context = "\n".join(
        [f"- {s['title']}: {s['content']}" for s in skills_to_use])

    if "latest" in model_id:  # LEGEND
        capability_prompt = f"""
        ĐẲNG CẤP MODEL: Gemini Latest (VIP).
        MỨC ĐỘ CHUYÊN NGHIỆP: CHUYÊN GIA ĐẦU NGÀNH.
        YÊU CẦU: 
        - Phân tích các kỹ năng dưới góc độ khoa học chuyên sâu.
        - Kết nối đa tầng giữa các kỹ năng đã nạp (Ví dụ: dùng Tư duy ngược để phân tích bài học Calisthenics).
        KỸ NĂNG ĐÃ NẠP:
        {skill_context}
        """

    elif "3-flash" in model_id:  # ARTISAN
        capability_prompt = f"""
        ĐẲNG CẤP MODEL: Gemini 3.0 (Pro).
        MỨC ĐỘ CHUYÊN NGHIỆP: CHUYÊN VIÊN THỰC THI.
        YÊU CẦU:
        - Đưa ra các ví dụ thực tế và bài tập áp dụng cho các kỹ năng.
        - Trình bày mạch lạc bằng Bullet points.
        KỸ NĂNG ĐÃ NẠP:
        {skill_context}
        """

    else:  # STANDARD
        capability_prompt = f"""
        ĐẲNG CẤP MODEL: Gemini 2.5 (Tiêu chuẩn).
        MỨC ĐỘ CHUYÊN NGHIỆP: CỘNG TÁC VIÊN NHIỆT TÌNH.
        YÊU CẦU:
        - Giải thích các kỹ năng một cách đơn giản, dễ hiểu nhất.
        - Tập trung vào những ý chính, cốt lõi của bài học.
        KỸ NĂNG ĐÃ NẠP:
        {skill_context}
        """

    # --------- 3. TỔNG HỢP ---------#
    full_prompt = f"""
    {capability_prompt}
    
    {persona_prompt}
    
    QUY TẮC: 
    1. Nếu có kỹ năng trong 'KỸ NĂNG ĐÃ NẠP', bắt buộc phải dùng kiến thức đó để trả lời.
    2. Luôn giữ đúng vai trò và đẳng cấp model.
    """

    return full_prompt
