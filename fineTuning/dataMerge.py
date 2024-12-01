import os
import json

folder_path = "fineTuning/data/1.Training/labeled_data" 

merged_data = []

for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"): 
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            merged_data.extend(data)  

output_file = "merged_train_data.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

