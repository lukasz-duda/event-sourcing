FROM python:3-alpine

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv /opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --requirement requirements.txt

COPY . .