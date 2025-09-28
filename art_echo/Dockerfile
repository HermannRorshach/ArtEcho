FROM python:3.12-slim
RUN groupadd -r groupmyuser && useradd -r -g groupmyuser myuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/artecho
RUN mkdir -p staticfiles && chown -R myuser:groupmyuser staticfiles

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chown -R myuser:groupmyuser /app/www/artecho/media/
RUN chmod -R 755 /app/www/artecho/media/
USER myuser