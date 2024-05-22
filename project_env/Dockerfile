FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY myproject /app/

# 포트 노출
EXPOSE 8000

# Django 개발 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]