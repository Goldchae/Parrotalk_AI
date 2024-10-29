import sys
import os

# chatgpt_prompting.py가 있는 디렉토리 경로 추가
sys.path.append(os.path.abspath('model/'))
from fastapi import FastAPI
from chatgpt_prompting import generate_sentence
import pandas as pd
import json

app = FastAPI()

# 데이터 파일 경로
file_path = 'data/Sample/01.원천데이터/1-014-046_sample(공감형대화).tsv'

# TSV 파일에서 데이터 읽기
phone_calls = pd.read_csv(file_path, sep='\t')

@app.get("/recommendations/")
async def get_recommendations(limit: int = 3):
    recommendation_results = []

    # 각 문장 데이터에 대해 누적해서 추천 문장 생성 수행
    for index, row in phone_calls.head(limit).iterrows():
        sentence = row['utterance_text']  # 'utterance_text'는 실제 열 이름으로 변경 필요
        result = generate_sentence(sentence.strip())

        # 분석 결과 저장
        analysis_result = {
            "dialogue": sentence.strip(),
            "추천 문장 1": result.get('추천 문장 1', 'N/A'),
            "추천 문장 2": result.get('추천 문장 2', 'N/A'),
            "추천 문장 3": result.get('추천 문장 3', 'N/A'),
        }
        recommendation_results.append(analysis_result)

    return {"recommendations": recommendation_results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
