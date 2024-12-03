from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# 모델과 토크나이저 불러오기 (초기화는 한 번만 수행!!)
model_name = "timpal0l/mdeberta-v3-base-squad2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

def get_base_model_answer(context, question):
    # 입력 데이터 토큰화
    inputs = tokenizer(question, context, return_tensors="pt")
    
    # 모델로부터 예측 결과 받기
    outputs = model(**inputs)
    answer_start_index = torch.argmax(outputs.start_logits)
    answer_end_index = torch.argmax(outputs.end_logits) + 1
    
    # 예측된 답변 토큰을 문자열로 변환
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start_index:answer_end_index])
    )
    
    return answer
