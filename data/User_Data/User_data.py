import hashlib

# --- 1. CƠ SỞ DỮ LIỆU NỘI BỘ (INTERNAL DATABASE) ---
USERS_DB = {
    "nikronos7": {
        "account": {
            "username": "nikronos7",
            "password": hashlib.sha256("@fairp26".encode()).hexdigest(),
            "gmail": "nikronos7.leader@gmail.com"
        },
        "general_settings": {
            "language": "Tiếng Việt",
            "theme": "Dark Mode"
        },
        "personalization": {
            "biometrics": {
                "weight_kg": 62.0,
                "height_cm": 172.0,
                "bmi": 20.9,
                "daily_water_target_liters": 2.5
            }
        },
        "payment_subscription": {
            "vnd_balance": 7000000,
            "fair_coin_balance": 1250,
            "current_tier": "Artisan (Premium)"
        }
    },
    "guest": {
        "account": {
            "username": "guest",
            "password": "none",  # Khách không cần mật khẩu
            "gmail": "guest.experience@fairp.io"
        },
        "general_settings": {
            "language": "Tiếng Việt",
            "theme": "Light Mode"
        },
        "personalization": {
            "biometrics": {
                "weight_kg": 55.0,
                "height_cm": 165.0,
                "bmi": 20.2,
                "daily_water_target_liters": 2.0
            }
        },
        "payment_subscription": {
            "vnd_balance": 50000,
            "fair_coin_balance": 10,
            "current_tier": "Standard Member"
        }
    }
}

# --- 2. CÁC HÀM TRUY XUẤT ---


def verify_login(username, password):
    """Kiểm tra đăng nhập từ USERS_DB"""
    u_key = username.lower().strip()
    if u_key in USERS_DB:
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        stored_password = USERS_DB[u_key]["account"]["password"]
        if hashed_input == stored_password:
            return True, USERS_DB[u_key]
    return False, None


def get_guest_data():
    """Lấy dữ liệu khách ngay lập tức"""
    return USERS_DB["guest"]
