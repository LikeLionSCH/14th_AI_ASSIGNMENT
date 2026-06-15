KEYWORD_TAGS = {
    "카페": ["카페", "커피", "디저트", "베이커리"],
    "맛집": ["맛집", "음식", "식당", "시장", "먹거리", "해장국", "김밥", "빵"],
    "사진": ["사진", "포토", "인생샷", "전망", "뷰", "풍경"],
    "감성": ["감성", "분위기", "예쁜", "아기자기", "골목"],
    "자연": ["자연", "숲", "공원", "정원", "꽃", "산"],
    "바다": ["바다", "해변", "해수욕장", "해안", "포구"],
    "산책": ["산책", "걷기", "둘레길", "해안도로"],
    "조용함": ["조용", "한적", "여유", "힐링", "쉬기"],
    "역사문화": ["역사", "문화", "전통", "한옥", "궁", "박물관", "유적"],
    "활동": ["활동", "체험", "레저", "놀이공원", "액티비티"],
    "실내": ["실내", "전시", "공연", "영화관"],
}

DISLIKE_KEYWORD_TAGS = {
    "혼잡함": ["사람", "많", "혼잡", "붐빔", "복잡"],
    "긴 도보": ["많이 걸", "힘들", "오르막", "계단", "멀"],
    "이동 불편": ["이동", "교통", "주차", "버스", "불편"],
    "높은 비용": ["비쌈", "비싸", "가격", "돈", "비용"],
    "긴 대기": ["대기", "줄", "기다"],
    "볼거리 부족": ["볼거리", "심심", "아쉬"],
    "날씨 영향": ["날씨", "비", "더위", "추위"],
}


def extract_tags(text: str, keyword_map: dict[str, list[str]]) -> list[str]:
    text = (text or "").lower()
    tags = []
    for tag, keywords in keyword_map.items():
        if any(keyword.lower() in text for keyword in keywords):
            tags.append(tag)
    return tags


def fallback_analyze_preference(record: dict) -> dict:
    liked_text = record.get("liked_text", "")
    disliked_text = record.get("disliked_text", "")
    diary_text = record.get("diary_text", "")
    memo = record.get("short_memo", "")
    favorite_place = record.get("favorite_place", "")
    satisfaction = int(record.get("satisfaction", 3))

    positive_source = " ".join([liked_text, diary_text, memo, favorite_place])
    negative_source = " ".join([disliked_text, diary_text, memo])

    preferred_tags = extract_tags(positive_source, KEYWORD_TAGS)
    disliked_tags = extract_tags(negative_source, DISLIKE_KEYWORD_TAGS)

    if satisfaction >= 4 and not preferred_tags:
        preferred_tags = ["만족도높음"]
    if satisfaction <= 2 and not disliked_tags:
        disliked_tags = ["만족도낮음"]

    travel_style = infer_style(preferred_tags)

    summary_parts = []
    if preferred_tags:
        summary_parts.append(f"선호 요소: {', '.join(preferred_tags)}")
    if disliked_tags:
        summary_parts.append(f"피하고 싶은 요소: {', '.join(disliked_tags)}")
    if liked_text:
        summary_parts.append(f"좋았던 점: {liked_text}")
    if disliked_text:
        summary_parts.append(f"아쉬웠던 점: {disliked_text}")
    if diary_text:
        summary_parts.append(f"여행 기록: {diary_text}")
    if memo:
        summary_parts.append(f"메모: {memo}")

    return {
        "preferred_tags": preferred_tags,
        "disliked_tags": disliked_tags,
        "favorite_place_type": [favorite_place] if favorite_place else [],
        "travel_style": travel_style,
        "satisfaction_summary": " / ".join(summary_parts) or "자연어 기록을 기반으로 취향을 분석했습니다.",
        "next_recommendation_direction": build_next_direction(
            preferred_tags, disliked_tags, travel_style
        ),
    }


def infer_style(preferred_tags: list[str]) -> str:
    tag_set = set(preferred_tags)
    if {"카페", "감성"} & tag_set:
        return "감성 카페형"
    if {"사진", "바다", "자연"} & tag_set:
        return "사진 기록형"
    if "맛집" in tag_set:
        return "맛집 탐방형"
    if {"조용함", "산책"} & tag_set:
        return "조용한 힐링형"
    if "역사문화" in tag_set:
        return "역사문화형"
    if "활동" in tag_set:
        return "활동형"
    return "균형 잡힌 여행형"


def build_next_direction(
    preferred_tags: list[str], disliked_tags: list[str], travel_style: str
) -> str:
    prefer = ", ".join(preferred_tags[:3]) if preferred_tags else "새로운 선호 요소"
    avoid = ", ".join(disliked_tags[:2]) if disliked_tags else "불편 요소"
    return f"{travel_style}에 맞춰 {prefer} 중심으로 추천하고, {avoid}는 줄이는 방향"
