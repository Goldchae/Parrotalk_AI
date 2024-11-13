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
작업: 대화하는 상황에서 문맥을 파악하여 문장단위 기준 맨 마지막 문장에 대한 답변하는 문장 3개를 반환해라.

추천 문장 1: 첫번째 문장
추천 문장 2: 두번쨰 문장
추천 문장 3: 세번째 문장


대화 내용: {text}
"""

def generate_sentence(dialogue_content):
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
    
#print(generate_sentence('오늘 날씨 춥더라'))