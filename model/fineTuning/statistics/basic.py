import json

file_paths = ["fineTuning/validate_data/base_model_validation.json",
              "fineTuning/validate_data/fineTuning_model_validation.json",
              "fineTuning/validate_data/gpt_model_validation.json"]

for file_path in file_paths:
  with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)
    scores = []
    for data in datas:
      scores.append(int(data["evaluation_score"]))
      
    # 평균 
    MEAN = sum(scores) / len(scores)

    # 중앙값
    scores.sort()
    MEDIAN = scores[len(scores)//2]

    # 분산
    VARIANCE = sum((x - MEAN) ** 2 for x in scores) / len(scores)

  print(f"{file_path}에 대한 결과:")
  print(f"평균 : {MEAN:.2f}")
  print(f"중앙값 : {MEDIAN:.2f}")
  print(f"분산 : {VARIANCE:.2f}")
  print()