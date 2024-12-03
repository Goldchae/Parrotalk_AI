from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
from transformers import AutoTokenizer

# 베이스 모델에서 토크나이저 로드
fine_tuned_tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-base")

fine_tuned_model_path = "results/checkpoint-12771" 

# 모델 로드
fine_tuned_model = AutoModelForQuestionAnswering.from_pretrained(fine_tuned_model_path)

def get_fineTuning_model_answer(context, question):
    
    # 입력 데이터 토큰화
    inputs = fine_tuned_tokenizer(question, context, return_tensors="pt")
    
    # 대답받기
    outputs = fine_tuned_model(**inputs)
    answer_start_index = torch.argmax(outputs.start_logits)
    answer_end_index = torch.argmax(outputs.end_logits) + 1
    
    # 답변 토큰 문자열로 변환
    answer = fine_tuned_tokenizer.convert_tokens_to_string(
        fine_tuned_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start_index:answer_end_index])
    )
    
    return answer
