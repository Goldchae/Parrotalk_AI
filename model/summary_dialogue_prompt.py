import logging
from dotenv import load_dotenv
import openai
import json
import os
from openai import OpenAI

# OpenAI API 키 설정
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 템플릿 문자열 정의
template_string = """
작업: 두명이 대화한 다음 대화록을 요약하고 대화록에 나온 '나'가 해야할 해야할일을 리스트화 해라

summary: 요약문
todo: 해야할일 목록
대화 내용: {text}
"""

def summary_dialogue(dialogue_content):
    # 템플릿 문자열을 대화 내용으로 완성
    prompt = template_string.format(text=dialogue_content)

    try:
        client = OpenAI(
            api_key=openai.api_key,
        )

        # OpenAI ChatGPT API를 호출하여 응답 받기
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Response in json format"},
                {"role": "user", "content": prompt}
            ],
            # response_format 지정하기
            response_format = {"type":"json_object"}
        )

        # 응답 메시지를 추출
        customer_response = response.choices[0].message.content

        # JSON 형식으로 파싱
        output_dict = json.loads(customer_response)

        return output_dict

    except Exception as e:
        # 오류가 발생할 경우 로깅
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return None
    
#사용예시

# dialogue=
# '''
# 오늘 점심에 뭐 먹을까? 나 피자 먹고 싶어! 같이 먹으러 가자. 좋아! 몇 시에 만날까? 12시에 학교 앞에서 만나자. 그래, 그럼 점심 전에 과제는 어떻게 할 거야? 나도 과제 시작해야 하는데, 어떤 주제로 할지 정했어? 나는 환경 오염에 대해 쓸 생각이야. 너는? 나는 AI의 영향력에 대해 쓸까 고민 중이야. 좋네! 그럼 주말에 자료 조사하고, 각자 숙제 해와서 점심 때 이야기해보자. 응, 그렇게 하자! 그럼 오늘 오후에 도서관에서 만나서 같이 할까? 좋아, 도서관에서 만나는 게 좋겠다. 그럼 3시에 도서관에서 보자! 오케이, 점심에 피자도 먹고 과제도 잘 준비하자! 맞아, 기대돼! 그럼 나중에 봐!
# '''
# print(summary_dialogue(dialogue))