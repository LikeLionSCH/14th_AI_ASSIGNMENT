import json

import pandas as pd
import streamlit as st

from src.data_loader import load_travel_logs
from src.profile_manager import load_profile

st.set_page_config(page_title="내 여행 취향", page_icon="👤", layout="wide")

st.title("내 여행 취향")
st.write("여행 기록에서 분석된 나의 여행 스타일과 선호 요소를 확인합니다.")

profile = load_profile()
logs = load_travel_logs()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("여행 스타일", profile.get("travel_style", "기록 없음"))
with col2:
    st.metric("저장된 기록", f"{len(logs):,}개")
with col3:
    st.metric("마지막 업데이트", profile.get("updated_at", "-"))

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("선호 요소")
    likes = profile.get("likes", [])
    if likes:
        st.write(", ".join(likes))
    else:
        st.info("아직 분석된 선호 요소가 없습니다.")

with right:
    st.subheader("피하고 싶은 요소")
    dislikes = profile.get("dislikes", [])
    if dislikes:
        st.write(", ".join(dislikes))
    else:
        st.info("아직 분석된 비선호 요소가 없습니다.")

st.divider()

st.subheader("최근 여행 기록")
if logs.empty:
    st.info("아직 저장된 여행 기록이 없습니다.")
else:
    display_columns = [
        "date",
        "visited_region",
        "visited_places",
        "satisfaction",
        "favorite_place",
        "ai_summary",
    ]
    existing_columns = [column for column in display_columns if column in logs.columns]
    st.dataframe(logs[existing_columns].tail(5), use_container_width=True)

    latest = logs.tail(1).iloc[0]
    st.subheader("최근 추천 방향")
    try:
        analysis = json.loads(latest["ai_preference_json"])
        st.write(analysis.get("next_recommendation_direction", "추천 방향 정보 없음"))
    except (TypeError, json.JSONDecodeError):
        st.write("최근 기록의 분석 JSON을 읽을 수 없습니다.")

    satisfaction = pd.to_numeric(logs["satisfaction"], errors="coerce").dropna()
    if not satisfaction.empty:
        st.metric("평균 만족도", f"{satisfaction.mean():.1f} / 5")

    st.divider()
    st.subheader("지역별 여행 기록 모아보기")
    st.write("방문 지역을 선택하면 그 지역에 남긴 여행 기록을 확인할 수 있습니다.")

    region_options = ["전체"] + sorted(logs["visited_region"].dropna().unique().tolist())
    selected_region = st.selectbox("방문 지역", region_options)

    if selected_region == "전체":
        selected_logs = logs.copy()
    else:
        selected_logs = logs[logs["visited_region"] == selected_region].copy()

    region_summary = (
        selected_logs.groupby("visited_region", dropna=False)
        .agg(
            record_count=("log_id", "count"),
            avg_satisfaction=("satisfaction", lambda s: pd.to_numeric(s, errors="coerce").mean()),
        )
        .reset_index()
        .sort_values("record_count", ascending=False)
    )
    st.dataframe(region_summary, use_container_width=True)

    for _, row in selected_logs.tail(10).iloc[::-1].iterrows():
        with st.container(border=True):
            st.markdown(f"### {row.get('favorite_place', '여행 기록')}")
            st.write(f"방문 지역: {row.get('visited_region', '-')}")
            st.write(f"방문 장소: {row.get('visited_places', '-')}")
            st.write(f"만족도: {row.get('satisfaction', '-')}/5")
            if pd.notna(row.get("short_memo")) and str(row.get("short_memo")).strip():
                st.write(str(row.get("short_memo")))
            if pd.notna(row.get("ai_summary")) and str(row.get("ai_summary")).strip():
                st.caption(str(row.get("ai_summary"))[:250])
