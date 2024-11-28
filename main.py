from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model.chatgpt_prompting import generate_sentence
from model.summary_dialogue_prompt import summary_dialogue
from model.recommend_check_prompt import recommend_check
from tts_model.google_tts import synthesize_speech_base64


app = FastAPI()

# 캐시 딕셔너리
cache = {}  # {"room_number": ["문장1", "문장2"]}
total_conversation_cache = {}  # {"room_number": ["전체 문장1", "전체 문장2"]}

# 문장 데이터를 위한 Pydantic 모델 정의
class DialogueRequest(BaseModel):
    room_number: str
    sentence: str

# TTS 요청 바디 스키마 정의
class TTSRequest(BaseModel):
    room_number: str
    voice_type: Literal["male1", "male2", "female1", "female2"]
    text: str

@app.get("/health")
async def health_check():
    return {"message": "Hello ParroTalk!"}

# 캐시에 문장 추가 (중복 확인)
def add_sentence_to_cache(room_number: str, sentence: str):
    # 캐시 초기화
    if room_number not in cache:
        cache[room_number] = []
    if room_number not in total_conversation_cache:
        total_conversation_cache[room_number] = []
    
    # 중복된 문장 추가 방지
    if not cache[room_number] or cache[room_number][-1] != sentence:
        cache[room_number].append(sentence)
    
    # 전체 대화 누적 캐시에 추가
    total_conversation_cache[room_number].append(sentence)

@app.post("/recommendations")
async def get_recommendations(request: DialogueRequest):
    sentence = request.sentence.strip()
    room_number = request.room_number

    try:
        # 문장 캐시에 추가
        add_sentence_to_cache(room_number, sentence)

        # 룸 넘버별 캐시에서 문장 조합
        combined_text = " ".join(cache[room_number])
        total_combined_text = " ".join(total_conversation_cache[room_number])  # 전체 누적 대화 텍스트

        # 추천 여부 판단
        is_recommend_combined = recommend_check(combined_text)

        if is_recommend_combined:
            # 추천 가능하면 캐시를 비우고 결과 반환
            cache[room_number].clear()

            # 추천 실행 (전체 누적 문장 활용)
            result = generate_sentence(total_combined_text)
            return {
                "room_number": room_number,
                "sentence": total_combined_text,
                "is_recommend": True,
                "recommendations": [
                    result.get('추천 문장 1', []),
                    result.get('추천 문장 2', []),
                    result.get('추천 문장 3', [])
                ]
            }
        else:
            # 추천 불가능하면 결합된 문장만 반환
            return {
                "room_number": room_number,
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

# Text-to-Speech API 엔드포인트
@app.post("/tts")
async def synthesize_tts(request: TTSRequest):
    try:
        # Google TTS 호출
        audio_base64 = synthesize_speech_base64(request.voice_type, request.text)
        return {"status": "success", "audio_base64": audio_base64}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8080)