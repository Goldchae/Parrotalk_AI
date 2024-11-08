import sys
import os
sys.path.append(os.path.abspath('model/'))
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatgpt_prompting import generate_sentence
from summary_dialogue_prompt import summary_dialogue
from recommend_check_prompt import recommend_check

app = FastAPI()

# 캐시 딕셔너리
cache = []  # 캐시는 리스트 형태로 선언합니다.
request_counter = 0  # 초기 카운터 값

# 문장 데이터를 위한 Pydantic 모델 정의
class DialogueRequest(BaseModel):
    room_number: str
    sentence: str
    
@app.get("/health")
async def health_check():
    return {"message": "Hello ParroTalk!"}

# 캐시에 문장 추가 (중복 확인)
def add_sentence_to_cache(sentence: str):
    if not cache or cache[-1] != sentence:  # 중복된 문장 추가 방지
        cache.append(sentence)
        
@app.post("/recommendations")
async def get_recommendations(request: DialogueRequest):
    global request_counter
    sentence = request.sentence.strip()

    try:
        # 문장 캐시에 추가
        add_sentence_to_cache(sentence)

        # 캐시에 저장된 모든 문장을 합쳐서 추천 여부 판단
        combined_text = " ".join(cache)

        is_recommend_combined = recommend_check(combined_text)

        if is_recommend_combined:
            # 추천 가능하면 캐시를 비우고 request_id 갱신
            request_counter += 1
            cache.clear()

            # 추천 실행
            result = generate_sentence(combined_text)
            return {
                "room_number": request.room_number,
                "sentence": combined_text,
                "is_recommend": True,
                "recommendations": [
                    result.get('추천 문장 1', []),
                    result.get('추천 문장 2', []),
                    result.get('추천 문장 3', [])
                ],
                #"request_id": request_counter
            }
        else:
            # 추천 불가능하면 결합된 문장만 반환
            return {
                "room_number": request.room_number,
                "sentence": combined_text,
                "is_recommend": False,
                "recommendations": []
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking recommendation: {str(e)}")
    
@app.post("/summary")
async def summarize_dialogue(request: DialogueRequest):
    dialogue_content = request.sentence.strip()

    if not dialogue_content:
        raise HTTPException(status_code=400, detail="Dialogue content cannot be empty.")

    summary_result = summary_dialogue(dialogue_content)

    if summary_result is None:
        raise HTTPException(status_code=500, detail="Failed to summarize dialogue.")
    
    return {
        "summary": summary_result['summary'],
        "todo": summary_result['todo']
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)