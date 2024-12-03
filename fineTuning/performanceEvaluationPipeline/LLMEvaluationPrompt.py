def make_LLM_evaluation_prompt(context, question, answer) :
    LLM_evaluation_prompt = f""" 
    전화 응답 적합성 평가
    
    아래 예시와 같이 통화 상황에서 상대방의 말에 대한 답변이 상황에 적합한지를 1,2,3,4,5,6,7,8,9,10의 숫자로 평가하시오.
    (10: 매우 적합, 1: 전혀 부적합)

    예시 1) 
    < 전화 통화 상황 >
    A: 반갑습니다 #@소속#입니다 무엇을 도와드릴까요 B: 네 #@상품# 주문 취소하려고 합니다 A: 네 고객님 성함과 전화번호는 어떻게 되실까요 B: #@이름#이고 휴대폰은 #@전번#이에요 
    < 상대방의 말 >
    네 고객님 #@상품# 구매하신 거로 확인되었습니다 취소하시겠습니까?
    < 피평가자의 답변 >
    네, 취소해주시면 감사하겠습니다.
    [당신의 평가]
    10

    예시 2) 
    < 전화 통화 상황 >
    A: 반갑습니다 #@소속#입니다 무엇을 도와드릴까요 B: 네 #@상품# 주문 취소하려고 합니다 A: 네 고객님 성함과 전화번호는 어떻게 되실까요 B: #@이름#이고 휴대폰은 #@전번#이에요 
    < 상대방의 말 >
    네 고객님 #@상품# 구매하신 거로 확인되었습니다 취소하시겠습니까?
    < 피평가자의 답변 >
    집에 가는 길을 알고 싶어요.
    [당신의 평가]
    1

    < 전화 통화 상황 >
    {context}
    < 상대방의 말 >
    {question}
    < 피평가자의 답변 >
    {answer}

    (반드시 답변을 숫자로만 할 것)
    """
    return LLM_evaluation_prompt
