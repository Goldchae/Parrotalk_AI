# 성능 평가 파이프라인
import json
import LLM_evalution_score
#import base_model_answer
#import fineTuning_model_answer
import gpt_model_answer
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false" # 콘솔창 더럽게 만드는 경고 메세지 삭!제!

# (키값) context, question, answer, evaluation_score
validate_datas = []


file_path = "fineTuning/data/2.Validation/cutted_validation_data.json"
 
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)
    for data in datas:
        validate_data = { "context":"","question":"","answer":"","evaluation_score":-1 }

        validate_data["context"] = data["context"]
        validate_data["question"] = data["question"]

        # 베이스 모델 응답
        # model_answer = base_model_answer.get_base_model_answer(data["context"], data["question"])
        # model_answer = fineTuning_model_answer.get_fineTuning_model_answer(data["context"], data["question"])
        model_answer = gpt_model_answer.get_gpt_model_answer(data["context"], data["question"])
        validate_data["answer"] = model_answer
        print("model_answer : " + model_answer)

        if model_answer in ["[CLS]", "[SEP]", ""]:
            validate_data["evaluation_score"] = "0"
            print("LLM_evaluation_score : " + "0")
        else:
            # LLM 검증
            LLM_evaluation_score =  LLM_evalution_score.get_LLM_evaluation_score(data["context"], data["question"], model_answer)
            validate_data["evaluation_score"] = LLM_evaluation_score
            print("LLM_evaluation_score : " + LLM_evaluation_score)

        validate_datas.append(validate_data)



# output_file = "base_model_validation.json"
# output_file = "fineTuning_model_validation.json"
output_file = "gpt_model_validation.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(validate_datas, file, ensure_ascii=False, indent=4)