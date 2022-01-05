FROM python:3-alpine

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --requirement requirements.txt

COPY ./warehouse/*.py /app/warehouse/

CMD [ "python", "-m", "unittest", "discover", "-s", "./warehouse", "-p", "*_test.py" ]