import json

merged_file_path = "fineTuning/data/1.Training/merged_train_data.json"

# JSON 데이터 정리 함수
def clean_json_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    cleaned_data = []
    for i, entry in enumerate(data):
        if not entry:  # entry가 None인 경우 제외
            print(f"Warning: Entry {i} is None. Skipping...")
            continue

        # 필수 필드 확인 및 기본 값 추가
        if "context" not in entry or not entry["context"]:
            print(f"Warning: Entry {i} missing 'context'. Skipping...")
            continue  # context가 없는 데이터는 제외
        if "question" not in entry or not entry["question"]:
            print(f"Warning: Entry {i} missing 'question'. Skipping...")
            continue  # question이 없는 데이터는 제외
        if "answers" not in entry or not isinstance(entry["answers"], dict):
            print(f"Warning: Entry {i} missing or invalid 'answers'. Setting default values...")
            entry["answers"] = {"text": [""], "answer_start": [0]}  # 기본 값 추가
        elif not entry["answers"]["text"]:  # answers["text"]가 비어 있는 경우
            print(f"Warning: Entry {i} has empty 'answers'. Setting default values...")
            entry["answers"]["text"] = [""]
            entry["answers"]["answer_start"] = [0]

        # 정리된 데이터를 추가
        cleaned_data.append(entry)

    # 정리된 데이터를 새로운 JSON 파일로 저장
    cleaned_file_path = "fineTuning/data/1.Training/cleaned_train_data.json"
    try:
        with open(cleaned_file_path, "w", encoding="utf-8") as cleaned_file:
            json.dump(cleaned_data, cleaned_file, ensure_ascii=False, indent=4)
        print(f"Cleaned data saved to: {cleaned_file_path}")
    except Exception as e:
        print(f"Error saving cleaned data: {e}")
        return None

    return cleaned_file_path

# JSON 데이터 정리 수행
cleaned_file_path = clean_json_data(merged_file_path)
if cleaned_file_path:
    print(f"Cleaned file path: {cleaned_file_path}")
else:
    print("Failed to clean and save JSON data.")
