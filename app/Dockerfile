FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --no-deps -r /code/requirements.txt

COPY ./ /code/app

CMD ["uvicorn", "app.main:backend", "--host", "0.0.0.0", "--port", "80"]