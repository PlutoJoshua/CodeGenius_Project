import classifier

# 분류할 질문 입력
user_prompt = input("질문을 입력하세요: ")

result = classifier.GOOGLEAI(user_prompt)

print(result)