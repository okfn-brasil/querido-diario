FROM node:slim

RUN npm install --quiet --global vue-cli

WORKDIR /mnt/code
RUN npm install -g nuxt \
    && npm install
CMD ["npm", "run", "dev"]
