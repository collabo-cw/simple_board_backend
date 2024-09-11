import os
from github import Github
from transformers import AutoTokenizer, AutoModelForCausalLM

# GitHub 액세스 토큰 설정
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
COMMIT_SHA = os.getenv('GITHUB_SHA')

# GitHub 클라이언트 초기화
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
commit = repo.get_commit(COMMIT_SHA)

# Mistral 7B 모델 로드
model_name = "mistralai/Mistral-7B-v0.1"
access_token = os.getenv('HF_TOKEN')
tokenizer = AutoTokenizer.from_pretrained(model_name, token=access_token)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", token=access_token)

# 변경된 파일 읽기 및 코드 리뷰 요청
for file in commit.files:
    if file.filename.endswith('.py'):  # Python 파일만 리뷰
        code = repo.get_contents(file.filename, ref=commit.sha).decoded_content.decode('utf-8')

        # 코드 리뷰 프롬프트 작성
        prompt = f"다음 Python 코드를 리뷰하고 개선점을 제안해 주세요:\n\n{code}\n\n리뷰 피드백:"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        # 모델 실행 및 리뷰 생성
        outputs = model.generate(**inputs, max_new_tokens=200, num_beams=1, early_stopping=True)
        review_feedback = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 커밋에 리뷰 코멘트 추가
        commit.create_comment(f"### 코드 리뷰 피드백 for `{file.filename}`:\n\n{review_feedback}")
