FROM node:18


RUN npm install -g truffle


WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["sh", "./deploy_and_run.sh"]
