from collections import Counter
from datetime import date

from src.config import DEFAULT_USER_ID, USER_PROFILE_PATH
from src.data_loader import load_json, save_json


def load_profile() -> dict:
    return load_json(USER_PROFILE_PATH)


def update_profile(analysis: dict) -> dict:
    profile = load_profile()

    like_counts = Counter(profile.get("like_counts", {}))
    dislike_counts = Counter(profile.get("dislike_counts", {}))

    like_counts.update(analysis.get("preferred_tags", []))
    dislike_counts.update(analysis.get("disliked_tags", []))

    profile.update(
        {
            "user_id": profile.get("user_id", DEFAULT_USER_ID),
            "travel_style": analysis.get("travel_style", profile.get("travel_style")),
            "likes": [tag for tag, _ in like_counts.most_common(8)],
            "dislikes": [tag for tag, _ in dislike_counts.most_common(8)],
            "like_counts": dict(like_counts),
            "dislike_counts": dict(dislike_counts),
            "updated_at": str(date.today()),
        }
    )
    save_json(USER_PROFILE_PATH, profile)
    return profile
