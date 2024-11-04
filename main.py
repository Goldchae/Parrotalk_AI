import sys
import os
sys.path.append(os.path.abspath('model/'))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatgpt_prompting import generate_sentence
#from recommend_check_judgement import recommend_check_judgement
from recommend_check_prompt import recommend_check

app = FastAPI()

# 캐시 딕셔너리
cache = {}

# 문장 데이터를 위한 Pydantic 모델 정의
class DialogueRequest(BaseModel):
    sentence: str

# 문장 데이터 모델 정의
class SentenceRequest(BaseModel):
    request_id: int
    sentence: str

@app.get("/health")
async def health_check():
    return {"message": "Hello ParroTalk!"}

@app.post("/recommendations")
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

# 문장 추가 함수
def add_sentence_to_cache(request_id: int, sentence: str):
    if request_id not in cache:
        cache[request_id] = []
    cache[request_id].append(sentence)
    
@app.post("/check")
async def check_recommendation(request: SentenceRequest):
    # 입력된 문장의 추천 가능 여부 확인
    request_id = request.request_id
    sentence = request.sentence.strip()
    
    try:
        # 문장 캐시에 추가
        add_sentence_to_cache(request_id, sentence)
        
        # 캐시에 저장된 문장들을 합쳐서 추천 가능 여부 판단
        combined_text = " ".join(cache[request_id])
        is_recommend = recommend_check(combined_text)
        
        # 추천 가능하면 캐시에서 삭제하여 초기화
        if is_recommend:
            del cache[request_id]
        
        return {
            "sentence": combined_text,
            "is_recommend": is_recommend,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking recommendation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)