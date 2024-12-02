import json
import os

def txt_to_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 대화 문맥 저장
    context = ""
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("A."):
            speaker, text = "A", line[2:].strip()
        elif line.startswith("B."):
            speaker, text = "B", line[2:].strip()
        else:
            continue
        
        context += f"{speaker}: {text} "
        
        # A, B 발화자 다르고, 뒷부분(끝에서 5줄)의 발화 내용 추출
        if speaker == "A" and i + 1 > len(lines)-5 and i + 1 < len(lines) and lines[i + 1].startswith("B."):
            next_text = lines[i + 1].strip()[2:].strip()
            return ({
                "id": f"{os.path.basename(file_path)}_{i}",
                "title": os.path.basename(file_path),
                "context": context.strip(),
                "question": text,
                "answers": {
                    "text": [next_text],
                    "answer_start": []
                }
            })

 #  JSON 파일 저장
def make_big_json(dialogues,file_path,output_dir):
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + ".json")
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(dialogues, json_file, ensure_ascii=False, indent=4)

# 실행
file_path_num = 409
none_cnt = 0
dialogues = []

output_dir = "./fineTuning/data/1.Training/labeled_data"
while True :
    if none_cnt > 10 :
        break
    try :
        file_path = f"./fineTuning/data/1.Training/source_data/TS_4.tourism/04.레저/tourism4_{file_path_num:04}.txt"
        dialogues.append(txt_to_json(file_path))
        file_path_num += 1
    except:
        file_path_num += 1
        none_cnt += 1
        continue
    

make_big_json(dialogues,file_path, output_dir)

# 정제 파일

#"./fineTuning/data/1.Training/labeled_data"
#"./fineTuning/data/1.Training/labeled_data"

# 원천 파일
#f"./fineTuning/data/1.Training/source_data/VS_1.shopping/01.AS문의/shopping1_{file_path_num:04}.txt"
#f"./fineTuning/data/1.Training/source_data/VS_1.shopping/02.제품사용문의/shopping2_{file_path_num:04}.txt"
#f"./fineTuning/data/1.Training/source_data/VS_1.shopping/03.주문결제/shopping3_{file_path_num:04}.txt"
#f"./fineTuning/data/1.Training/source_data/VS_1.shopping/04.배송/shopping4_{file_path_num:04}.txt"
#f"./fineTuning/data/1.Training/source_data/VS_1.shopping/05.환불반품교환/shopping5_{file_path_num:04}.txt"
#f"./fineTuning/data/1.Training/source_data/VS_1.shopping/06.이벤트/shopping6_{file_path_num:04}.txt"
#f"./fineTuning/data/1.Training/source_data/VS_1.shopping/07.온오프라인안내/shopping7_{file_path_num:04}.txt"
