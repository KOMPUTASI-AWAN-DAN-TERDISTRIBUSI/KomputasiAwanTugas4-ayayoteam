FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1

WORKDIR /app

# Dependency untuk message_queue (pyzmq) dan reticulum_announce (rns).
# rpc/ hanya memakai standard library, tidak perlu tambahan.
RUN pip install --no-cache-dir pyzmq rns

COPY . /app

CMD ["python", "--version"]