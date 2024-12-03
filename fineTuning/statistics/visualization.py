import json
import matplotlib.pyplot as plt

data_summary = []
compare = []

file_paths = ["fineTuning/validate_data/base_model_validation.json",
              "fineTuning/validate_data/gpt_model_validation.json"]

for file_path in file_paths:
  with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)
    scores = []
    for data in datas:
      scores.append(int(data["evaluation_score"]))
    compare.append(scores)
    # 평균 
    MEAN = sum(scores) / len(scores)

    # 중앙값
    scored = sorted(scores)
    MEDIAN = scored[len(scores)//2]

    # 분산
    VARIANCE = sum((x - MEAN) ** 2 for x in scores) / len(scores)
    data_summary.append((file_path.split('/')[-1], MEAN, MEDIAN, VARIANCE))
print(compare)
print(data_summary)

labels = [item[0] for item in data_summary]
means = [item[1] for item in data_summary]
medians = [item[2] for item in data_summary]
variances = [item[3] for item in data_summary]


# 평균 막대 그래프
fig1, ax1 = plt.subplots()
ax1.bar(labels, means, color='blue', label='Mean')
ax1.set_xlabel('Model')
ax1.set_ylabel('Scores')
ax1.set_title('Mean')
ax1.legend()

# 중앙값 막대 그래프
fig2, ax2 = plt.subplots()
ax2.bar(labels, medians, color='green', label='Median')
ax2.set_xlabel('Model')
ax2.set_ylabel('Scores')
ax2.set_title('Median')
ax2.legend()


# 분산 막대 그래프
fig3, ax3 = plt.subplots()
ax3.bar(labels, variances, label='Variance', color='red')
ax3.set_xlabel('Model')
ax3.set_ylabel('Variance')
ax3.set_title('Variance')
ax3.legend()


# 값 비교
data1 = compare[0]
data2 = compare[1]
plt.figure(figsize=(10, 5))  # 그래프 크기 설정
plt.plot( data1, label='Data 1', marker='o', color='red')
plt.plot( data2, label='Data 2', marker='o', color='blue')  
plt.ylabel('Value')     
plt.legend()                 
plt.grid(True)              

plt.show()
