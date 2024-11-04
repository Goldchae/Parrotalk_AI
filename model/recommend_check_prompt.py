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
작업: 다음은 상대방의 문장이다. 다음문장에 대하여 답변가능여부를 판단하세요.


문장끝맺음이 안끝났으면 False를 반환, 완전문장이면 True를 반환,
질문형태이며 True를 반환, 답변가능한 문장이면 True를 반환
예를 들어, '배고파': True, '오늘': False, '오늘 하루 힘들다':True
check_sentence: True/False
excuse: 이유
sentence: {text}
"""

def recommend_check(dialogue_content):
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

        # 응답 메시지를 JSON으로 추출
        customer_response = response.choices[0].message.content

        # JSON 응답 파싱하여 추천 여부 추출
        try:
            response_json = json.loads(customer_response)
            output = response_json.get("check_sentence", False)
            # output2 = response_json.get("excuse", False)
            # return response_json
            return output
        except json.JSONDecodeError:
            print("응답을 JSON으로 파싱하는 데 실패했습니다.")
            output = False

        return output

    except Exception as e:
        # 오류가 발생할 경우 로깅
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return None
    
    
#sentence='나는 오늘 학교에 갔다.'
#sentence='나는'
#sentence='배고파 나는 오늘 학교에 갔다 근데 점심이 쏘야였어. 너의 학교 점심은 뭐였어'
#print(is_recommend(sentence))