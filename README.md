# Simple_Board DRF Side Project
백엔드 연습을 위한 사이드 프로젝트

## 개요
DRF의 익숙해지기 위해 만듦

## 구조
```
┌── core
│   │   ├── migrations
│   │   │   └── ...
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── simple_board_backend
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user
│   │   ├── migrations
│   │   │   └── ...
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── .gitignore
├── LICENSE
├── manage.py
├── requirements.txt
└── ... 
```

## 데이터베이스
Postgresql version 3.10 ++

구현 해야 할 테이블
> 유저
>
> 관리자
> 
> 게시판
> 
> 게시판 카테고리
> 
> 게시판 유저 관계
> 
> 댓글
> 
> 게시판 이미지 첨부파일
> 
> 추천 or 좋아요 < 이부분은 아직 구현할지 미지수

## 기술 스택
Django 4.2++ , DRF 3.15 ++

## 구현할 기능

* 회원 가입 기능
* 로그인, 로그아웃 기능
* 게시판 메인
* 게시판 글쓰기, 수정
* 게시판 상세
* 댓글