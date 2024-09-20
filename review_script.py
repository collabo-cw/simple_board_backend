import os
from github import Github
import replicate

# GitHub 액세스 토큰 설정
GIT_TOKEN = os.getenv('GIT_TOKEN')
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY')

# GitHub 클라이언트 초기화
g = Github(GIT_TOKEN)
repo_name = os.getenv('GITHUB_REPOSITORY')
commit_sha = os.getenv('GITHUB_SHA')
repo = g.get_repo(repo_name)
commit = repo.get_commit(commit_sha)

# Replicate 클라이언트 초기화
client = replicate.Client(api_token=REPLICATE_API_KEY)
model = "mistralai/Mistral-7b-v0.1"  # Mistral 7B 모델

# 변경된 파일들에 대해 코드 리뷰 수행
for file in commit.files:
    if file.filename.endswith('.py'):  # Python 파일만 리뷰
        code = repo.get_contents(file.filename, ref=commit.sha).decoded_content.decode('utf-8')

        # 코드 리뷰 요청을 위한 프롬프트 작성
        prompt = f"다음 Python 코드를 리뷰하고 개선할 점을 제안해 주세요:\n\n{code}"

        # Replicate API 호출하여 리뷰 결과 생성
        output = client.run(
            model,
            input={"prompt": prompt, "new_max_tokens": 200}
        )

        # GitHub 커밋에 리뷰 코멘트 추가
        commit.create_comment(f"### 코드 리뷰 피드백 for `{file.filename}`:\n\n{output}")