from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate,  HumanMessagePromptTemplate

recommend_system_message = '''### 지시 ###
주어지는 문장은 내 전화 상대방의 문장이다. 맥락에 따른 답변 추천 예시를 3개 생성하라.

### 출력 형식 ###
json 형식으로 출력하되 아래 형식으로 출력하라.
{{
    "recommend": [
        // 요약한 메시지 3개, 이는 겹치면 안 된다.
    ]
}}
### 출력 형식 ###
그들의 이전 대화 내용 :
'''

def make_recommend_prompt(partner_input, history) :
    recommend_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template( recommend_system_message + "{HISTORY}"),
            HumanMessagePromptTemplate.from_template("{PARTNER_INPUT}"),
        ]
    ).format(PARTNER_INPUT=partner_input, HISTORY= history)
    return recommend_prompt