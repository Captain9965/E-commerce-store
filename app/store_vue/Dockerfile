FROM node:16-slim


RUN mkdir /vue_app
WORKDIR /vue_app
RUN npm install -g http-server
RUN npm install i -g serve
COPY package*.json ./
RUN npm install
COPY . .