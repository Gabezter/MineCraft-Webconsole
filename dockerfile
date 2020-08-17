FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /opt/Minecraft/
RUN mkdir /opt/Minecraft/server
RUN mkdir /opt/Minecraft/server/plugins
COPY ./test /opt/Minecraft/server/plugins


COPY . .

CMD [ "sh", "./start.sh" ]