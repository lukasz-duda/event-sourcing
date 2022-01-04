FROM python:3-alpine

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --requirement requirements.txt

COPY *.py /app/

CMD [ "pytest", "account_test.py" ]