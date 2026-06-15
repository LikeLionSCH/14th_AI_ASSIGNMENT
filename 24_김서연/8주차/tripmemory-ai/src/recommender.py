from src.data_loader import split_tags

TRAVEL_TYPE_TAGS = {
    "감성 카페형": ["감성", "카페", "사진", "조용함"],
    "사진 기록형": ["사진", "감성", "전망", "골목"],
    "맛집 탐방형": ["맛집", "시장", "카페"],
    "조용한 힐링형": ["조용함", "자연", "산책", "바다"],
    "역사문화형": ["역사문화", "전통", "박물관"],
    "활동형": ["활동", "체험", "걷기", "야외"],
}

LEVEL_SCORE = {
    ("적게 걷기", "낮음"): 2,
    ("적게 걷기", "보통"): 0,
    ("적게 걷기", "높음"): -2,
    ("보통", "낮음"): 1,
    ("보통", "보통"): 2,
    ("보통", "높음"): 0,
    ("많이 걷기", "낮음"): 0,
    ("많이 걷기", "보통"): 1,
    ("많이 걷기", "높음"): 2,
}

BUDGET_SCORE = {
    ("낮음", "낮음"): 2,
    ("낮음", "보통"): 0,
    ("낮음", "높음"): -2,
    ("보통", "낮음"): 1,
    ("보통", "보통"): 2,
    ("보통", "높음"): 0,
    ("높음", "낮음"): 0,
    ("높음", "보통"): 1,
    ("높음", "높음"): 2,
}


def score_place(place, conditions: dict, profile: dict | None = None) -> tuple[int, list[str]]:
    reasons = []
    score = 0

    place_tags = split_tags(place.get("tags", ""))
    place_mood = split_tags(place.get("mood", ""))
    searchable = set(place_tags + place_mood + [str(place.get("category", ""))])

    target_tags = TRAVEL_TYPE_TAGS.get(conditions["travel_type"], [])
    matched_type_tags = [tag for tag in target_tags if tag in searchable]
    if matched_type_tags:
        score += len(matched_type_tags) * 3
        reasons.append(f"여행 유형과 맞는 태그: {', '.join(matched_type_tags)}")

    walking_score = LEVEL_SCORE.get(
        (conditions["walking_preference"], place.get("walking_level")), 0
    )
    score += walking_score
    if walking_score > 0:
        reasons.append("도보 선호도와 잘 맞음")

    budget_score = BUDGET_SCORE.get((conditions["budget"], place.get("budget_level")), 0)
    score += budget_score
    if budget_score > 0:
        reasons.append("예산 조건과 잘 맞음")

    if profile:
        liked_matches = [tag for tag in profile.get("likes", []) if tag in searchable]
        disliked_matches = [tag for tag in profile.get("dislikes", []) if tag in searchable]
        if liked_matches:
            score += len(liked_matches) * 2
            reasons.append(f"기존 선호 취향 반영: {', '.join(liked_matches[:3])}")
        if disliked_matches:
            score -= len(disliked_matches) * 3
            reasons.append(f"피하고 싶은 요소와 일부 겹침: {', '.join(disliked_matches[:2])}")

    selected_region = conditions.get("region", "전국")
    selected_district = conditions.get("district", "전체")

    if selected_region != "전국" and str(place.get("city")) == selected_region:
        score += 2
        reasons.append("선택한 시/도의 장소")
    elif selected_region == "전국":
        score += 1
        reasons.append("전국 후보에 포함된 장소")

    if selected_district != "전체" and str(place.get("district")) == selected_district:
        score += 2
        reasons.append("선택한 시/군/구의 장소")

    if not reasons:
        reasons.append("기본 조건을 기준으로 추천")

    return score, reasons


def recommend_places(places, conditions: dict, profile: dict | None = None, limit: int = 5):
    selected_region = conditions.get("region", "전국")
    selected_district = conditions.get("district", "전체")

    if selected_region == "전국":
        filtered = places.copy()
    else:
        filtered = places[places["city"] == selected_region].copy()
        if selected_district != "전체":
            filtered = filtered[filtered["district"] == selected_district].copy()
        if filtered.empty:
            filtered = places.copy()

    scored_rows = []
    for _, place in filtered.iterrows():
        score, reasons = score_place(place, conditions, profile)
        row = place.to_dict()
        row["score"] = score
        row["recommendation_reason"] = " / ".join(reasons)
        scored_rows.append(row)

    return sorted(
        scored_rows,
        key=lambda item: (
            item.get("score", 0),
            item.get("visit_count", 0) if item.get("visit_count") == item.get("visit_count") else 0,
            item.get("avg_satisfaction", 0)
            if item.get("avg_satisfaction") == item.get("avg_satisfaction")
            else 0,
        ),
        reverse=True,
    )[:limit]


def make_recommendation_title(conditions: dict) -> str:
    region = conditions.get("region", "전국")
    district = conditions.get("district", "전체")
    area = region if district == "전체" else f"{region} {district}"
    return f"{area} {conditions['travel_type']} 여행지 추천"
