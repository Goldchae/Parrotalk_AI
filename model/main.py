from chatgpt_prompting import generate_sentence
import json
import pandas as pd

'''

to do
- 실제 데이터 가져오기
- 누적해서 맥락파악
- 글자수 제한 고려(채팅창 디스프레이 고려)

'''

# data 파일 경로
file_path = 'data/Sample/01.원천데이터/1-014-046_sample(공감형대화).tsv'

phone_calls = pd.read_csv(file_path, sep='\t')
phone_calls = phone_calls.head(3)
recommendation_results = []

# 각 문장데이터 에 대해 누적해서 추천 문장 생성 수행
for index, row in phone_calls.iterrows():
    sentence = row['utterance_text'] 

    result = generate_sentence(sentence.strip())
    
    # 분석 결과 저장
    analysis_result = {
        "dialogue": sentence.strip(),
        "추천 문장 1": result.get('추천 문장 1', 'N/A'),
        "추천 문장 2": result.get('추천 문장 2', 'N/A'),
        "추천 문장 3": result.get('추천 문장 3', 'N/A'),
    }
    recommendation_results.append(analysis_result)


# 결과 출력
for result in recommendation_results:
    print(json.dumps(result, ensure_ascii=False, indent=4))

# 결과를 json 파일로 저장 (선택적)
# with open('phishing_analysis_results.json', 'w', encoding='utf-8') as f:
#     json.dump(phishing_analysis_results, f, ensure_ascii=False, indent=4)