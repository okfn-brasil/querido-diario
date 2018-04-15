FROM node:9.11.1-slim

ENV HOME=/mnt/code
ENV HOST 0.0.0.0
ENV PORT 8080

RUN npm install --quiet --global nuxt vue-cli

COPY package*.json $HOME/

WORKDIR $HOME
RUN npm install

COPY . $HOME

RUN npm run build
CMD ["npm", "run", "dev"]
