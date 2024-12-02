<<<<<<< HEAD
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, Trainer, TrainingArguments
from datasets import load_dataset

# 모델과 토크나이저 불러오기
model_name = "timpal0l/mdeberta-v3-base-squad2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# 데이터셋 로드
dataset = load_dataset("path/to/your/dataset.json", format="json")

# 파인튜닝 설정
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['validation']
)

# 파인튜닝 시작
trainer.train()
=======
from datasets import Dataset
from transformers import AutoTokenizer

from transformers import AutoModelForQuestionAnswering, Trainer, TrainingArguments

import torch



# 병합된 JSON 파일 경로
merged_file_path = "fineTuning/data/1.Training/cleaned_train_data.json"

# 데이터셋 로드
dataset = Dataset.from_json(merged_file_path)

# DeBERTa v3 모델용 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/deberta-v3-base",
    use_fast=False,  # 빠른 토크나이저 사용
)

# 전처리 함수 정의
def preprocess_function(examples):
    contexts = examples["context"]
    questions = examples["question"]
    answers = examples["answers"]

    inputs = tokenizer(
        contexts,
        questions,
        max_length=512,  # 최대 길이 설정
        truncation=True,  # 긴 텍스트는 자름
        padding="max_length",  # 고정 길이로 패딩
    )

    start_positions = []
    end_positions = []

    for context, answer_list in zip(contexts, answers):
        # `answers`의 구조를 처리
        if not answer_list or not isinstance(answer_list, dict) or "text" not in answer_list:
            # answers가 비어 있거나 잘못된 경우 기본값 설정
            start_positions.append(0)
            end_positions.append(0)
            continue

        answer_texts = answer_list["text"]  # 답변 텍스트 리스트
        if len(answer_texts) == 0 or not answer_texts[0]:
            # 답변이 없는 경우 기본값 설정
            start_positions.append(0)
            end_positions.append(0)
            continue

        # 첫 번째 답변의 시작 위치 계산
        answer = answer_texts[0]
        start = context.find(answer)
        if start == -1:  # 답변이 context에 포함되지 않는 경우
            start_positions.append(0)
            end_positions.append(0)
        else:
            start_positions.append(start)
            end_positions.append(start + len(answer))

    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions

    return inputs


# 전처리 함수 적용
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# DeBERTa v3 모델 로드
model = AutoModelForQuestionAnswering.from_pretrained("microsoft/deberta-v3-base")

# 학습 설정 정의
training_args = TrainingArguments(
    output_dir=".fineTuning/results",  # 결과 저장 폴더
    evaluation_strategy="no",  # 에폭마다 평가
    learning_rate=2e-5,  # 학습률
    per_device_train_batch_size=8,  # 배치 크기
    num_train_epochs=3,  # 학습 에폭 수
    weight_decay=0.01,  # 가중치 감쇠
    save_total_limit=2,  # 최대 저장 체크포인트 수
    fp16=True,  # GPU 사용 시 mixed precision 활성화
)

# Trainer 정의
trainer = Trainer(
    model=model,  # 모델
    args=training_args,  # 학습 설정
    train_dataset=tokenized_dataset,  # 학습 데이터
)

# GPU 사용 가능 여부 확인
if torch.cuda.is_available():
    print(f"GPU 사용 가능: {torch.cuda.get_device_name(0)}")
else:
    print("GPU를 사용할 수 없습니다. CPU로 학습이 진행됩니다.")


# 학습 시작
trainer.train()

>>>>>>> origin/newBranch
