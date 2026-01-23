import hashlib

# --- 1. CƠ SỞ DỮ LIỆU NỘI BỘ ---
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
        },
        # [MỚI] Dữ liệu điểm số học kỳ
        "learning_results": {
            "grades": [
                {"subject": "Toán học", "tx1": 9.5, "tx2": 9.8,
                    "tx3": 9.0, "tx4": 9.5, "midterm": 9.6, "final": 0.0},
                {"subject": "Ngữ văn", "tx1": 8.0, "tx2": 8.2,
                    "tx3": 7.8, "tx4": 8.5, "midterm": 8.0, "final": 0.0},
                {"subject": "Tiếng Anh", "tx1": 9.0, "tx2": 9.5,
                    "tx3": 9.2, "tx4": 9.0, "midterm": 9.4, "final": 0.0},
                {"subject": "Vật lý", "tx1": 9.0, "tx2": 9.2, "tx3": 8.8,
                    "tx4": 9.5, "midterm": 9.1, "final": 0.0},
                {"subject": "Hóa học", "tx1": 8.5, "tx2": 8.8,
                    "tx3": 9.0, "tx4": 8.5, "midterm": 8.7, "final": 0.0},
                {"subject": "Tin học", "tx1": 10.0, "tx2": 10.0,
                    "tx3": 9.8, "tx4": 10.0, "midterm": 9.9, "final": 0.0}
            ]
        }
    },
    "guest": {
        "account": {
            "username": "guest",
            "password": "none",
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
        },
        # [MỚI] Dữ liệu điểm số khách (Demo)
        "learning_results": {
            "grades": [
                {"subject": "Toán học", "tx1": 7.5, "tx2": 8.0,
                    "tx3": 7.0, "tx4": 7.5, "midterm": 7.8, "final": 0.0},
                {"subject": "Ngữ văn", "tx1": 7.0, "tx2": 7.5,
                    "tx3": 7.2, "tx4": 7.0, "midterm": 7.3, "final": 0.0},
                {"subject": "Tiếng Anh", "tx1": 6.5, "tx2": 7.0,
                    "tx3": 6.8, "tx4": 7.0, "midterm": 6.9, "final": 0.0},
                {"subject": "Vật lý", "tx1": 8.0, "tx2": 7.5, "tx3": 8.2,
                    "tx4": 8.0, "midterm": 7.9, "final": 0.0},
                {"subject": "Hóa học", "tx1": 7.0, "tx2": 7.2,
                    "tx3": 7.0, "tx4": 7.5, "midterm": 7.1, "final": 0.0},
                {"subject": "Tin học", "tx1": 8.5, "tx2": 9.0,
                    "tx3": 8.8, "tx4": 9.0, "midterm": 8.9, "final": 0.0}
            ]
        }
    }
}

# --- 2. CÁC HÀM TRUY XUẤT ---


def verify_login(username, password):
    u_key = username.lower().strip()
    if u_key in USERS_DB:
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        stored_password = USERS_DB[u_key]["account"]["password"]
        if hashed_input == stored_password:
            return True, USERS_DB[u_key]
    return False, None


def get_guest_data():
    return USERS_DB["guest"]
