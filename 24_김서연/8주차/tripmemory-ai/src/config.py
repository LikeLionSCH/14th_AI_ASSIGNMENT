from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

PLACES_PATH = PROCESSED_DIR / "places.csv"
TRAVEL_LOGS_PATH = PROCESSED_DIR / "travel_logs.csv"
USER_PROFILE_PATH = PROCESSED_DIR / "user_profile.json"

DEFAULT_USER_ID = "default_user"

TRAVEL_TYPES = [
    "감성 카페형",
    "사진 기록형",
    "맛집 탐방형",
    "조용한 힐링형",
    "역사문화형",
    "활동형",
]

COMPANION_TYPES = ["혼자", "친구", "연인", "가족"]
WALKING_LEVELS = ["적게 걷기", "보통", "많이 걷기"]
BUDGET_LEVELS = ["낮음", "보통", "높음"]

LIKED_TAG_OPTIONS = [
    "감성적인 분위기",
    "사진 찍기 좋음",
    "맛집",
    "카페",
    "자연",
    "바다",
    "전통/역사",
    "조용함",
    "활동적임",
    "실내 위주",
]

DISLIKED_TAG_OPTIONS = [
    "사람이 많음",
    "많이 걸음",
    "이동이 불편함",
    "비쌈",
    "볼거리가 적음",
    "날씨 영향이 큼",
    "음식이 아쉬움",
    "대기 시간이 김",
]
