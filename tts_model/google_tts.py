import os
from google.cloud import texttospeech
from datetime import datetime
import base64

# FastAPI 애플리케이션 초기화
#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./stt-test-key.json"

# Google TTS 처리 함수
def synthesize_speech_base64(voice_type: str, text: str) -> str:
    # Google Cloud Text-to-Speech 클라이언트 초기화
    client = texttospeech.TextToSpeechClient()

    # 목소리 매핑 설정
    voice_map = {
        "female1": {"language_code": "en-AU", "name": "en-AU-Journey-O"},
        "female2": {"language_code": "en-AU", "name": "en-AU-Journey-F"},
        "male1": {"language_code": "en-AU", "name": "en-AU-Journey-D"},
        "male2": {"language_code": "en-GB", "name": "en-GB-Journey-D"},
    }

    if voice_type not in voice_map:
        raise ValueError(f"Invalid voice type '{voice_type}'. Choose from: {', '.join(voice_map.keys())}")

    # 음성 설정
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_map[voice_type]["language_code"],
        name=voice_map[voice_type]["name"]
    )

    # 오디오 설정
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Text-to-Speech 요청
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # 오디오 데이터를 base64로 인코딩
    audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
    
    # 현재 날짜와 시간으로 파일 이름 생성
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_filename = f"outputvoice_{timestamp}.mp3"

    # 결과 파일 저장 (선택 사항)
    # os.makedirs("audio", exist_ok=True)
    # filepath = os.path.join("audio", output_filename)
    # with open(filepath, "wb") as out:
    #     out.write(response.audio_content)
    #     print(f"Audio content written to file '{filepath}'")

    # base64 인코딩된 데이터를 반환
    return audio_base64
