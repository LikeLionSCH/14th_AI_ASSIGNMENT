import pandas as pd
import streamlit as st

from src.config import BUDGET_LEVELS, COMPANION_TYPES, TRAVEL_TYPES, WALKING_LEVELS
from src.data_loader import load_places
from src.profile_manager import load_profile
from src.recommender import make_recommendation_title, recommend_places

st.set_page_config(page_title="여행지 추천", page_icon="🧭", layout="wide")

places = load_places()
profile = load_profile()

st.title("여행지 추천")
st.write("원하는 지역과 여행 조건을 선택하면 AI Hub 여행로그 데이터 기반으로 어울리는 여행지를 추천합니다.")

regions = ["전국"] + sorted(places["city"].dropna().unique().tolist())
categories = ["전체"] + sorted(places["category"].dropna().unique().tolist())

with st.sidebar:
    st.subheader("추천 후보 필터")
    min_visits = st.slider("최소 방문 횟수", 1, 20, 1)
    category_filter = st.selectbox("카테고리", categories)
    st.caption(f"전체 후보: {len(places):,}개")

filtered_places = places[pd.to_numeric(places["visit_count"], errors="coerce").fillna(0) >= min_visits]
if category_filter != "전체":
    filtered_places = filtered_places[filtered_places["category"] == category_filter]

area_col1, area_col2 = st.columns(2)
with area_col1:
    region = st.selectbox("도/광역시", regions)
with area_col2:
    if region == "전국":
        district_options = ["전체"]
    else:
        district_options = ["전체"] + sorted(
            places[places["city"] == region]["district"].dropna().unique().tolist()
        )
    district = st.selectbox("시/군/구", district_options)

with st.form("recommend_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        travel_type = st.selectbox("여행 유형", TRAVEL_TYPES)
    with col2:
        travel_time = st.selectbox("여행 기간", ["반나절", "하루", "1박 2일", "2박 3일 이상"])
        companion_type = st.selectbox("동행 유형", COMPANION_TYPES)
    with col3:
        walking_preference = st.selectbox("도보 선호도", WALKING_LEVELS)
        budget = st.selectbox("예산", BUDGET_LEVELS, index=1)

    use_profile = st.checkbox("내 여행 취향 프로필 반영", value=True)
    submitted = st.form_submit_button("추천 결과 보기")

if submitted:
    conditions = {
        "region": region,
        "district": district,
        "travel_time": travel_time,
        "travel_type": travel_type,
        "companion_type": companion_type,
        "walking_preference": walking_preference,
        "budget": budget,
    }
    active_profile = profile if use_profile else None
    recommendations = recommend_places(filtered_places, conditions, active_profile, limit=5)

    st.subheader(make_recommendation_title(conditions))
    st.caption("취향 프로필 반영됨" if use_profile else "현재 선택 조건만 반영됨")

    if not recommendations:
        st.warning("조건에 맞는 추천 후보가 없습니다. 필터를 조금 넓혀보세요.")
    else:
        for index, place in enumerate(recommendations, start=1):
            score = int(place.get("score", 0))
            visit_count = int(place.get("visit_count", 0)) if pd.notna(place.get("visit_count")) else 0
            satisfaction = place.get("avg_satisfaction")
            recommendation = place.get("avg_recommendation")

            with st.container(border=True):
                header_col, score_col = st.columns([4, 1])
                with header_col:
                    district_text = f" {place.get('district')}" if pd.notna(place.get("district")) else ""
                    st.markdown(f"### {index}. {place['place_name']}")
                    st.write(f"{place.get('city', '-')}{district_text}")
                with score_col:
                    st.metric("추천 점수", score)

                st.write(place.get("description", "설명 없음"))

                meta1, meta2, meta3, meta4 = st.columns(4)
                meta1.metric("카테고리", place.get("category", "-"))
                meta2.metric("방문 횟수", f"{visit_count:,}")
                meta3.metric("만족도", f"{float(satisfaction):.2f}" if pd.notna(satisfaction) else "-")
                meta4.metric("추천 의향", f"{float(recommendation):.2f}" if pd.notna(recommendation) else "-")

                st.write(
                    f"도보: {place.get('walking_level', '-')} / "
                    f"예산: {place.get('budget_level', '-')} / "
                    f"혼잡도: {place.get('crowd_level', '-')}"
                )
                if place.get("address") and pd.notna(place.get("address")):
                    st.write(f"주소: {place['address']}")
                st.write(f"추천 이유: {place['recommendation_reason']}")

        result_df = pd.DataFrame(recommendations)
        st.download_button(
            "추천 결과 CSV 다운로드",
            result_df.to_csv(index=False, encoding="utf-8-sig"),
            file_name="tripmemory_recommendations.csv",
            mime="text/csv",
        )
else:
    st.info("조건을 선택하고 추천 결과 보기를 누르면 여행지 추천이 표시됩니다.")
