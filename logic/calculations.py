import streamlit as st
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
    Tự động xác định Model dựa trên Hạng thành viên (Tier) và Gói mua lẻ.
    """

    # 1. TỰ ĐỘNG TÍNH RANK (Single Source of Truth)
    # Lấy dữ liệu ví tiền trực tiếp
    pay_data = st.session_state.get('payment_data', {})
    current_tier = pay_data.get('current_tier', 'Standard Member')

    # Định nghĩa Rank của Hạng thành viên
    TIER_RANK = {
        "Standard Member": 0,
        "Artisan (Premium)": 1,
        "Legend (Elite)": 2
    }
    tier_rank = TIER_RANK.get(current_tier, 0)

    # Lấy Rank của Model mua lẻ (nếu có)
    bought_rank = st.session_state.get('bought_model_rank', 0)

    # Rank thực tế = Cái nào cao hơn thì lấy
    final_rank = max(tier_rank, bought_rank)

    # 2. XÁC ĐỊNH "THÁI ĐỘ" (Persona) THEO SỨC KHỎE
    if readiness_score >= 80:
        mode_label = "Power Mode ⚡"
        mode_color = "success"  # Xanh lá
    elif readiness_score >= 50:
        mode_label = "Balanced ⚖️"
        mode_color = "info"    # Xanh dương
    else:
        mode_label = "Supportive ❤️"
        mode_color = "warning"  # Vàng

    # 3. QUYẾT ĐỊNH MODEL ID (Dựa trên Final Rank đã tính ở bước 1)

    # --- LEVEL 2: LEGEND / VIP ---
    if final_rank >= 2:
        return f"Gemini Latest ({mode_label})", mode_color, "models/gemini-flash-latest"

    # --- LEVEL 1: ARTISAN / 3.0 ---
    elif final_rank >= 1:
        return f"Gemini 3.0 Flash ({mode_label})", mode_color, "models/gemini-3-flash-preview"

    # --- LEVEL 0: STANDARD ---
    else:
        # Standard thì dùng bản 2.5 Flash
        return f"Gemini 2.5 Flash ({mode_label})", mode_color, "models/gemini-2.5-flash"


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
