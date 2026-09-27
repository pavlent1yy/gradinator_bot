FROM python:3.12-slim

ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1

# tzdata для корректного часового пояса (МСК)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends tzdata curl \
	&& rm -rf /var/lib/apt/lists/* \
	&& ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
	&& echo $TZ > /etc/timezone

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m botuser && chown -R botuser /app
USER botuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
	CMD python -c "import os; exit(0 if os.getenv('BOT_TOKEN') else 1)"

CMD ["python", "bot.py"]
