import sys
import os
sys.path.append(os.path.abspath('model/'))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatgpt_prompting import generate_sentence

app = FastAPI()

# 문장 데이터를 위한 Pydantic 모델 정의
class DialogueRequest(BaseModel):
    sentence: str

@app.get("/health")
async def health_check():
    return {"message": "Hello ParroTalk!"}

@app.post("/recommendations/")
async def get_recommendations(request: DialogueRequest):
    # 입력된 문장을 처리하여 추천 문장 3개 생성
    result = generate_sentence(request.sentence.strip())
    
    # 결과가 없을 때 예외 처리
    if not result:
        raise HTTPException(status_code=500, detail="Fail to Recommendation")
    
    # 추천 문장을 JSON 형식으로 반환
    analysis_result = {
        "dialogue": request.sentence.strip(),
        "추천 문장 1": result.get('추천 문장 1', 'N/A'),
        "추천 문장 2": result.get('추천 문장 2', 'N/A'),
        "추천 문장 3": result.get('추천 문장 3', 'N/A'),
    }
    
    return {"recommendations": analysis_result}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8080)