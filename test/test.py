import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import recommend_service

print("장미꽃은 다른 이름으로 불리워져도 똑같이 향기로울 게 아닌가?")
print(recommend_service.recommend(1,"장미꽃은 다른 이름으로 불리워져도 똑같이 향기로울 게 아닌가?"))