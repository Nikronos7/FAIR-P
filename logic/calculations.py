def calculate_readiness(data):
    """
    Tính chỉ số Sẵn sàng Học tập (Readiness Score) dựa trên công thức:
    Readiness = Sleep + Exercise - Stress + Water
    """

    # 1. Sleep Score = (Giờ ngủ / 8) * Chất lượng (1-6)
    sleep_h = data.get('sleep_hours', 0)
    sleep_q = data.get('sleep_quality', 0)
    sleep_score = (sleep_h / 8.0) * sleep_q

    # 2. Exercise Bonus = Điểm vận động (0, 1.0, 1.5, 2.0)
    exercise_bonus = data.get('exercise_score', 0)

    # 3. Stress Penalty = Trừ trực tiếp điểm Stress (0, 1, 2, 3)
    stress_penalty = data.get('stress_score', 0)

    # 4. Water Bonus (Tiêu chuẩn 3L)
    # >= 3L (100%) -> +2 điểm
    # >= 1.5L (50%) -> +1 điểm
    water_val = data.get('water_consumed', 0)
    water_bonus = 0
    if water_val >= 3.0:
        water_bonus = 2
    elif water_val >= 1.5:
        water_bonus = 1

    # --- TỔNG HỢP ---
    raw_score = sleep_score + exercise_bonus - stress_penalty + water_bonus

    # Quy đổi sang thang 100 (Vì max lý thuyết ~10 điểm)
    final_score = raw_score * 10

    # Kẹp giá trị trong khoảng 0-100 để không bị lố
    return int(max(0, min(final_score, 100)))


def get_ai_mode(readiness_score):
    """
    Trả về: (Tên hiển thị, Màu sắc, ID Model kỹ thuật)
    """
    if readiness_score >= 80:
        # Model mạnh và ổn định nhất cho trạng thái đỉnh cao
        return "Gemini Flash (Power Mode)", "success", "models/gemini-flash-latest"

    elif readiness_score >= 50:
        # Model cân bằng
        return "Gemini 2.5 Flash (Balanced)", "info", "models/gemini-2.5-flash"

    else:
        # Model nhẹ nhàng cho lúc mệt
        return "Gemini Flash Lite (Supportive)", "warning", "models/gemini-flash-lite-latest"
