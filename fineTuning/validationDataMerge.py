import os
import json

folder_path = "fineTuning/data/2.Validation/labeled_data"

fixed_data = []
 
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        # 20개 파일, 200개 데이터 목표, 한 파일당 10개씩 뽑기
        cutted_data = data[:20]
        fixed_data.extend(cutted_data)

output_file = "cutted_validation_data.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(fixed_data, file, ensure_ascii=False, indent=4)