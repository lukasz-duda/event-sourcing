FROM python:3-alpine

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --requirement requirements.txt

COPY *.py /app/

CMD [ "python", "-m", "unittest", "discover", "-p", "*_test.py" ]