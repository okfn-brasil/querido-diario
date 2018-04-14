FROM node:slim

RUN npm install --quiet --global vue-cli

WORKDIR /mnt/code
RUN npm install -g nuxt
COPY package*.json /mnt/code/
RUN npm install
COPY . /mnt/code
RUN npm build
CMD ["npm", "start"]
