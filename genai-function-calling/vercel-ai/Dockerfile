FROM node:22-alpine

WORKDIR /app

COPY package.json /app/

RUN touch .env && npm install

COPY *.js /app/

ENTRYPOINT ["npm", "start"]
