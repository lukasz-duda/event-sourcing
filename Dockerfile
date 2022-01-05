FROM python:3-alpine

WORKDIR /warehouse
COPY requirements.txt /warehouse/

RUN pip install --upgrade pip
RUN pip install --requirement requirements.txt

COPY warehouse/*.py /warehouse/

CMD [ "python", "-m", "unittest", "discover", "-p", "*_test.py" ]