FROM node:16-slim as build-stage


RUN mkdir /vue_app
WORKDIR /vue_app
# RUN npm install -g http-server
RUN npm install i -g serve
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine as production-stage

#remove default index.html page
RUN rm -rf /usr/share/nginx/html/*

COPY --from=build-stage /vue_app/dist /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]