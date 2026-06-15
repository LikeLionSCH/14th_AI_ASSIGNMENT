import json
from datetime import date

import streamlit as st

from src.ai_analyzer import fallback_analyze_preference
from src.config import DEFAULT_USER_ID
from src.data_loader import append_travel_log, join_tags, load_places
from src.profile_manager import update_profile

st.set_page_config(page_title="여행 기록 작성", page_icon="📝", layout="wide")

st.title("여행 기록 작성")
st.write("하루의 여행을 기록하듯 남겨보세요. 기록 속 좋았던 점과 불편했던 점은 다음 추천에 반영됩니다.")

places = load_places()
regions = sorted(places["city"].dropna().unique().tolist())

area_col1, area_col2 = st.columns(2)
with area_col1:
    visited_region = st.selectbox("방문한 도/광역시", regions)
with area_col2:
    districts = ["전체"] + sorted(
        places[places["city"] == visited_region]["district"].dropna().unique().tolist()
    )
    visited_district = st.selectbox("방문한 시/군/구", districts)

region_places = places[places["city"] == visited_region]
if visited_district != "전체":
    region_places = region_places[region_places["district"] == visited_district]
place_options = sorted(region_places["place_name"].dropna().unique().tolist())

with st.form("travel_log_form"):
    col1, col2 = st.columns(2)
    with col1:
        log_title = st.text_input("기록 제목", placeholder="예: 비 오는 날의 광안리 산책")
        visited_places = st.multiselect("방문 장소", place_options)
        favorite_options = visited_places if visited_places else place_options
        favorite_place = st.selectbox("가장 기억에 남는 장소", favorite_options)
        satisfaction = st.slider("전체 만족도", min_value=1, max_value=5, value=4)

    with col2:
        liked_text = st.text_area(
            "좋았던 순간",
            placeholder="예: 바다 전망이 좋았고 사진 찍기 좋은 곳이 많았어요. 카페 분위기도 조용해서 쉬기 좋았습니다.",
            height=130,
        )
        disliked_text = st.text_area(
            "불편했던 점",
            placeholder="예: 사람이 너무 많아서 대기 시간이 길었고, 주차가 조금 불편했어요.",
            height=130,
        )

    diary_text = st.text_area(
        "여행 기록",
        placeholder="오늘의 여행을 자유롭게 기록해보세요. 어떤 장소를 갔고, 어떤 분위기였고, 다음에 다시 가고 싶은지 적어도 좋아요.",
        height=220,
    )
    submitted = st.form_submit_button("기록 저장하기")

if submitted:
    record = {
        "visited_region": visited_region,
        "visited_district": visited_district,
        "visited_places": visited_places,
        "satisfaction": satisfaction,
        "log_title": log_title,
        "diary_text": diary_text,
        "liked_text": liked_text,
        "disliked_text": disliked_text,
        "favorite_place": favorite_place,
        "short_memo": diary_text,
    }

    analysis = fallback_analyze_preference(record)
    updated_profile = update_profile(analysis)

    append_travel_log(
        {
            "user_id": DEFAULT_USER_ID,
            "date": str(date.today()),
            "visited_region": visited_region
            if visited_district == "전체"
            else f"{visited_region} {visited_district}",
            "visited_places": join_tags(visited_places),
            "satisfaction": satisfaction,
            "liked_tags": join_tags(analysis["preferred_tags"]),
            "disliked_tags": join_tags(analysis["disliked_tags"]),
            "favorite_place": favorite_place,
            "next_travel_style": analysis["travel_style"],
            "short_memo": f"{log_title}\n\n{diary_text}".strip(),
            "ai_summary": analysis["satisfaction_summary"],
            "ai_preference_json": json.dumps(analysis, ensure_ascii=False),
        }
    )

    st.success("여행 기록이 저장되었고, 취향 프로필이 업데이트되었습니다.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("이번 기록에서 발견한 취향")
        st.write(f"여행 스타일: {analysis['travel_style']}")
        st.write(f"좋아하는 요소: {', '.join(analysis['preferred_tags']) or '아직 뚜렷하지 않음'}")
        st.write(f"피하고 싶은 요소: {', '.join(analysis['disliked_tags']) or '아직 뚜렷하지 않음'}")
    with col2:
        st.subheader("다음 추천 방향")
        st.write(analysis["next_recommendation_direction"])
        st.caption("분석 결과는 내 여행 취향에 누적 반영됩니다.")
else:
    st.info("여행 기록을 쌓으면 내 여행 취향 페이지에서 지역별 기록을 모아볼 수 있습니다.")
