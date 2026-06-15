import os
from dotenv import load_dotenv
import google.genai as genai

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()

# Gemini API 키를 환경 변수에서 가져옵니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("오류: GEMINI_API_KEY 환경 변수를 찾을 수 없습니다.")
else:
    try:
        print("genai.Client 객체를 생성하고 client.models 속성을 확인합니다...")
        # Client 클래스를 사용하여 API 클라이언트를 초기화합니다.
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        print("\n" + "="*15 + " dir(client.models) 결과 " + "="*15)
        # client.models 객체가 가진 모든 속성과 메소드 목록을 출력합니다.
        print(dir(client.models))
        print("="*50)

    except Exception as e:
        print(f"\n오류가 발생했습니다: {e}")