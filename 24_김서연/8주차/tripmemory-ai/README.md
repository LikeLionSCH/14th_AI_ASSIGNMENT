# TripMemory AI

TripMemory AI는 AI Hub 국내 여행로그 경량 데이터를 활용해 사용자의 여행 조건과 여행 기록을 바탕으로 국내 여행지를 추천하는 Streamlit 웹앱입니다.

이 프로젝트는 링크로 접속 가능한 간단한 제출용 웹앱을 목표로 합니다. 사용자는 원하는 지역과 여행 조건을 선택해 여행지를 추천받고, 여행 후 기록을 남기면 앱이 자연어 기록에서 여행 취향을 분석해 다음 추천에 반영합니다.

## 프로젝트 목적

- AI Hub 여행로그 데이터를 추천 서비스에 활용해보기
- 사용자의 여행 조건에 맞는 여행지 추천 구현
- 자연어 여행 기록에서 선호/비선호 요소 추출
- 누적된 여행 기록을 기반으로 개인화 추천 흐름 설계
- Streamlit을 이용해 웹앱 형태로 결과물 제출

## 사용 데이터

사용 데이터는 AI Hub의 국내 여행로그 경량 데이터입니다.

앱에서는 원본 전체 데이터를 직접 사용하지 않고, 방문지정보 데이터를 전처리한 `places.csv`를 사용합니다.

전처리 과정에서 활용한 주요 정보:

- 방문 장소명
- 주소 및 좌표
- 방문지 유형
- 방문 횟수
- 만족도
- 재방문 의향
- 추천 의향
- 체류 시간
- 소비 금액

원본 데이터 폴더는 용량이 크기 때문에 배포에는 포함하지 않고, 전처리된 CSV만 사용합니다.

## 주요 기능

- 전국 및 지역별 여행지 추천
- 도/광역시 선택 후 시/군/구 선택
- 여행 유형, 예산, 도보 선호도 기반 추천
- 사용자 취향 프로필 반영 추천
- 여행 기록 작성
- 자연어 기록 기반 취향 분석
- 지역별 여행 기록 모아보기
- 추천 결과 CSV 다운로드

## AI 활용 방식

현재 버전은 외부 LLM API를 사용하지 않습니다.

대신 사용자가 작성한 여행 기록 문장에서 키워드를 분석해 선호 요소와 비선호 요소를 추출하는 fallback 분석 로직을 구현했습니다.

예시:

```text
입력: 바다 전망이 좋고 사진 찍기 좋았다. 사람이 많고 주차가 불편했다.

분석 결과:
- 선호 요소: 바다, 사진
- 비선호 요소: 혼잡함, 이동 불편
- 여행 스타일: 사진 기록형
```

이 분석 결과는 `user_profile.json`에 누적되고, 여행지 추천 점수 계산에 반영됩니다.

## 추천 방식

추천 로직은 태그 기반 점수 계산 방식입니다.

점수에 반영되는 요소:

- 사용자가 선택한 여행 유형
- 도보 선호도
- 예산
- 여행지 카테고리
- 여행지 태그와 분위기
- 사용자 선호 태그
- 사용자 비선호 태그

선호 태그와 여행지 태그가 일치하면 가산점을 주고, 비선호 태그와 겹치면 감점합니다.

## 화면 구성

### Home

- 서비스 소개
- 추천 가능한 여행지 수
- 반영된 방문 기록 수
- 현재 분석된 취향 요약

### 여행지 추천

- 도/광역시 선택
- 시/군/구 선택
- 여행 유형 선택
- 여행 기간, 동행 유형, 도보 선호도, 예산 선택
- 추천 여행지 TOP 5 출력

### 여행 기록 작성

- 방문 지역 선택
- 방문 장소 선택
- 기록 제목 작성
- 좋았던 순간 입력
- 불편했던 점 입력
- 다이어리 형식의 여행 기록 작성
- 저장 후 취향 분석 결과를 사용자용 문장으로 표시

### 내 여행 취향

- 현재 여행 스타일 확인
- 선호 요소와 비선호 요소 확인
- 최근 여행 기록 확인
- 지역별 여행 기록 모아보기

## 실행 방법

프로젝트 폴더로 이동합니다.

```bash
cd tripmemory-ai
```

필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

Streamlit 앱을 실행합니다.

```bash
streamlit run app.py
```

브라우저가 자동으로 열리지 않으면 아래 주소로 접속합니다.

```text
http://localhost:8501
```

## 배포 방법

Streamlit Community Cloud 배포를 기준으로 합니다.

1. GitHub 저장소에 프로젝트 업로드
2. Streamlit Community Cloud에서 새 앱 생성
3. Repository, branch, main file path 입력
4. main file path는 `app.py`로 설정
5. Deploy 클릭

배포에 포함할 주요 파일:

```text
app.py
pages/
src/
data/processed/places.csv
data/processed/travel_logs.csv
data/processed/user_profile.json
requirements.txt
README.md
```

배포에서 제외해도 되는 파일/폴더:

```text
여행로그데이터_수도권/
여행로그데이터_동부/
여행로그데이터_서부/
여행로그데이터_제주/
__pycache__/
```

## 데이터 전처리

AI Hub 경량 데이터를 다시 전처리하려면 아래 명령을 실행합니다.

```bash
python scripts/build_places_from_aihub.py
```

생성되는 파일:

```text
data/processed/places_aihub.csv
data/processed/places.csv
```

전처리 과정에서 지역명은 표준화합니다.

예시:

- 경기, 경기도 -> 경기도
- 부산, 부산광역시 -> 부산광역시
- 강원, 강원도 -> 강원특별자치도
- 경남, 경상남도 -> 경상남도

## 폴더 구조

```text
tripmemory-ai/
├── app.py
├── pages/
│   ├── 1_여행지추천.py
│   ├── 2_여행기록작성.py
│   └── 3_내여행취향.py
├── src/
│   ├── ai_analyzer.py
│   ├── config.py
│   ├── data_loader.py
│   ├── profile_manager.py
│   └── recommender.py
├── scripts/
│   └── build_places_from_aihub.py
├── data/
│   └── processed/
│       ├── places.csv
│       ├── places_aihub.csv
│       ├── travel_logs.csv
│       └── user_profile.json
├── notebooks/
│   └── TripMemory_AI_AIHUB_전처리_추천.ipynb
├── requirements.txt
└── README.md
```

## 저장 방식과 한계

현재 앱은 별도 데이터베이스를 사용하지 않고 로컬 파일에 데이터를 저장합니다.

- 여행 기록: `data/processed/travel_logs.csv`
- 사용자 취향: `data/processed/user_profile.json`

로컬 실행에서는 페이지를 새로고침하거나 다시 접속해도 기록이 유지됩니다. 다만 배포 환경에서는 서버 재시작이나 재배포 상황에 따라 파일 저장이 안정적으로 유지되지 않을 수 있습니다.

실제 서비스로 확장한다면 Supabase, SQLite, PostgreSQL 같은 데이터베이스를 연결하는 것이 적합합니다.

## 향후 개선 방향

- 실제 LLM API를 연결한 자연어 취향 분석 고도화
- 사용자별 로그인 및 프로필 분리
- 데이터베이스 연동
- 지도 기반 방문 기록 시각화
- 지역별 추천 성능 개선
- 추천 이유 문장 고도화
