import json
from datetime import date

import pandas as pd

from src.config import (
    DEFAULT_USER_ID,
    PLACES_PATH,
    PROCESSED_DIR,
    TRAVEL_LOGS_PATH,
    USER_PROFILE_PATH,
)

TRAVEL_LOG_COLUMNS = [
    "log_id",
    "user_id",
    "date",
    "visited_region",
    "visited_places",
    "satisfaction",
    "liked_tags",
    "disliked_tags",
    "favorite_place",
    "next_travel_style",
    "short_memo",
    "ai_summary",
    "ai_preference_json",
]


def ensure_data_files() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if not TRAVEL_LOGS_PATH.exists():
        pd.DataFrame(columns=TRAVEL_LOG_COLUMNS).to_csv(
            TRAVEL_LOGS_PATH, index=False, encoding="utf-8-sig"
        )

    if not USER_PROFILE_PATH.exists():
        default_profile = {
            "user_id": DEFAULT_USER_ID,
            "travel_style": "아직 충분한 기록이 없어요",
            "likes": [],
            "dislikes": [],
            "like_counts": {},
            "dislike_counts": {},
            "preferred_budget": "보통",
            "preferred_walking": "보통",
            "updated_at": str(date.today()),
        }
        save_json(USER_PROFILE_PATH, default_profile)


def load_places() -> pd.DataFrame:
    ensure_data_files()
    return pd.read_csv(PLACES_PATH, encoding="utf-8-sig")


def load_travel_logs() -> pd.DataFrame:
    ensure_data_files()
    return pd.read_csv(TRAVEL_LOGS_PATH, encoding="utf-8-sig")


def append_travel_log(log_data: dict) -> None:
    ensure_data_files()
    logs = load_travel_logs()
    next_id = 1 if logs.empty else int(logs["log_id"].max()) + 1
    log_data = {"log_id": next_id, **log_data}
    updated_logs = pd.concat([logs, pd.DataFrame([log_data])], ignore_index=True)
    updated_logs.to_csv(TRAVEL_LOGS_PATH, index=False, encoding="utf-8-sig")


def load_json(path):
    ensure_data_files()
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def split_tags(value) -> list[str]:
    if pd.isna(value) or value == "":
        return []
    return [tag.strip() for tag in str(value).split("|") if tag.strip()]


def join_tags(tags: list[str]) -> str:
    return "|".join(tags)
