FROM python:3.8.0

RUN pip install pipenv

WORKDIR /botapp
COPY ./Pipfile /botapp/

RUN pipenv install --system --skip-lock

COPY . /botapp/

EXPOSE 8000

CMD python slabot/server.py
