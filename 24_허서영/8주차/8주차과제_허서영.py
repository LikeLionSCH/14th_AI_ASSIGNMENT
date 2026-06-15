import os
from dotenv import load_dotenv
import google.genai as genai

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()

# Gemini API 키를 환경 변수에서 가져옵니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("오류: GEMINI_API_KEY 환경 변수를 찾을 수 없습니다.")
    print(".env 파일에 키가 올바르게 설정되었는지 확인해주세요.")
    exit()

try:
    # Client 클래스를 사용하여 API 클라이언트를 초기화합니다.
    client = genai.Client(api_key=GEMINI_API_KEY)

    print("="*60)
    print("코드 해설사 AI에 오신 것을 환영합니다! (Gemini ver.)")
    print("설명을 원하는 코드 한 조각을 입력해주세요.")
    print("입력을 마치려면 빈 줄에서 Enter 키를 두 번 누르세요.")
    print("="*60)

    # 여러 줄의 코드를 입력받습니다.
    lines = []
    while True:
        try:
            line = input()
            if not line:
                # 사용자가 Enter만 두 번 눌러 입력을 종료했는지 확인
                if not lines or not lines[-1]:
                    break
                lines.append(line)
            else:
                lines.append(line)
        except EOFError:
            break

    # 입력이 끝난 후 마지막의 빈 줄 제거
    if lines and not lines[-1]:
        lines.pop()

    code_to_explain = "\n".join(lines).strip()

    if not code_to_explain:
        print("\n입력된 코드가 없습니다. 프로그램을 종료합니다.")
    else:
        print("\nAI가 코드를 분석하고 있습니다. 잠시만 기다려주세요...")

        # AI에게 보낼 프롬프트를 구성합니다.
        prompt = f"""
        당신은 '코드 해설사' AI입니다. 
        사용자가 입력한 아래 코드의 역할과 작동 방식을 한국어로 쉽고 명확하게 설명해주세요. 
        주요 로직, 각 변수의 의미, 함수의 목적 등을 단계별로 풀어서 설명해주세요.
        신입 개발자나 비전공자도 이해할 수 있도록 친절한 말투를 사용해주세요.

        --- 분석할 코드 ---
        {code_to_explain}
        --- 코드 설명 ---
        """

        try:
            # client.models에서 바로 generate_content를 호출하고,
            # 모델 이름과 프롬프트를 파라미터로 전달합니다.
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )

            # AI의 답변을 추출하여 출력합니다.
            explanation = response.text
            print("\n" + "="*25 + " AI의 코드 설명 " + "="*25)
            print(explanation)
            print("="*69)

        except Exception as e:
            print(f"\n콘텐츠 생성 중 오류가 발생했습니다: {e}")
            print("API 키가 정확한지, 네트워크 연결이 정상인지 확인해주세요.")

except Exception as e:
    print(f"\n초기화 중 오류가 발생했습니다: {e}")
    print("API 키를 확인하거나 라이브러리 설치 상태를 다시 확인해주세요.")