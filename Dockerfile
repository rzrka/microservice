FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV APP_MODULE server:app

COPY ./ /app

RUN pip install --upgrade pip && \
    pip install -r /app/req.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
