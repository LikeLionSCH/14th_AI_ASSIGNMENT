import pandas as pd
import streamlit as st

from src.data_loader import ensure_data_files, load_places, load_travel_logs
from src.profile_manager import load_profile

st.set_page_config(page_title="TripMemory AI", page_icon="✈️", layout="wide")

ensure_data_files()
places = load_places()
profile = load_profile()
logs = load_travel_logs()

visit_total = int(pd.to_numeric(places.get("visit_count", 0), errors="coerce").fillna(0).sum())
avg_satisfaction = pd.to_numeric(places.get("avg_satisfaction"), errors="coerce").mean()

st.title("TripMemory AI")
st.markdown(
    "여행 기록과 취향을 바탕으로 다음 여행에 어울리는 국내 여행지를 추천해주는 개인화 여행 추천 서비스입니다."
)

st.write(
    "여행 후 느낀 점을 짧게 남기면 TripMemory AI가 선호 요소와 피하고 싶은 요소를 분석합니다. "
    "분석된 취향은 다음 여행지 추천에 반영되어, 사용할수록 나에게 더 맞는 추천을 받을 수 있습니다."
)

st.divider()

metric1, metric2, metric3 = st.columns(3)
metric1.metric("추천 가능한 여행지", f"{len(places):,}개")
metric2.metric("반영된 방문 기록", f"{visit_total:,}건")
metric3.metric("평균 만족도", f"{avg_satisfaction:.2f}" if pd.notna(avg_satisfaction) else "-")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("여행지 추천")
    st.write("지역, 여행 유형, 예산, 도보 선호도를 선택해 지금 가기 좋은 여행지를 찾아보세요.")
    st.page_link("pages/1_여행지추천.py", label="추천받기", icon="🧭")

with col2:
    st.subheader("여행 기록 작성")
    st.write("좋았던 점과 아쉬웠던 점을 자연어로 남기면 취향 프로필이 업데이트됩니다.")
    st.page_link("pages/2_여행기록작성.py", label="기록 남기기", icon="📝")

with col3:
    st.subheader("내 여행 취향")
    st.write("지금까지의 여행 기록에서 분석된 나의 여행 스타일과 선호 요소를 확인하세요.")
    st.page_link("pages/3_내여행취향.py", label="취향 보기", icon="👤")

st.divider()

left, right = st.columns([1, 1])
with left:
    st.subheader("현재 분석된 취향")
    st.write(f"여행 스타일: {profile.get('travel_style', '아직 충분한 기록이 없어요')}")
    st.write(f"선호 요소: {', '.join(profile.get('likes', [])) or '아직 없음'}")
    st.write(f"피하고 싶은 요소: {', '.join(profile.get('dislikes', [])) or '아직 없음'}")

with right:
    st.subheader("저장된 기록")
    st.metric("여행 기록 수", f"{len(logs):,}개")
    st.write("기록이 쌓일수록 추천 결과가 더 개인화됩니다.")
