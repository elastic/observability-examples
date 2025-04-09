FROM node:22-alpine

WORKDIR /app
COPY package.json *.js /app/
RUN touch .env && npm install

ENTRYPOINT ["npm", "start"]
