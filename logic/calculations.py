import pandas as pd
from datetime import datetime
import os


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


def save_daily_progress(score):
    # Lưu vào thư mục data/User_Data như trong ảnh thư mục của bạn
    folder_path = 'data/User_Data'
    file_path = f'{folder_path}/progress_log.csv'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    new_entry = pd.DataFrame(
        [[datetime.now().strftime('%d/%m'), score]], columns=['Ngày', 'Readiness'])

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Nếu hôm nay đã có điểm rồi thì cập nhật điểm mới nhất
        if df.empty or df.iloc[-1]['Ngày'] != new_entry.iloc[0]['Ngày']:
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df.iloc[-1, 1] = score
    else:
        df = new_entry

    df.to_csv(file_path, index=False)


def get_progress_data():
    file_path = 'data/User_Data/progress_log.csv'
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None
