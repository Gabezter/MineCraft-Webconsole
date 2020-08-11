FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=development
ENV FLASK_APP=/usr/src/app/__init__.py:app

CMD [ "sh", "./start.sh" ]