FROM node:22-alpine

WORKDIR /app
COPY package.json index.js /app/
RUN touch .env && npm install

CMD ["npm", "start"]
