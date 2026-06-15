# AI 코드 해설사

이 프로젝트는 사용자가 입력한 코드 조각을 AI를 사용하여 설명해주는 간단한 파이썬 스크립트입니다.

## 주요 기능

-   여러 줄의 코드 입력을 지원합니다.
-   Google Gemini API를 사용하여 코드 설명을 생성합니다.

## 설정 방법

1.  **저장소 복제 (Clone Repository):**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **라이브러리 설치 (Install Dependencies):**
    `requirements.txt` 파일에 명시된 필수 라이브러리를 설치합니다.
    ```bash
    pip3 install -r requirements.txt
    ```

3.  **환경 변수 설정 (Environment Variables):**
    `.env`라는 파일을 이 폴더 안에 생성하고, 아래와 같이 Gemini API 키를 추가합니다. API 키는 [Google AI Studio](https://aistudio.google.com/)에서 발급받을 수 있습니다.
    ```
    GEMINI_API_KEY="여기에_발급받은_API_키를_입력하세요"
    ```

## 실행 방법

터미널에서 아래 명령어를 실행합니다.
```bash
python3 main.py
```
