FROM node:9.11.1-slim

ENV HOME /mnt/code
ENV HOST 0.0.0.0
ENV PORT 8080

COPY package*.json $HOME/
WORKDIR $HOME
RUN npm install

COPY . $HOME
EXPOSE $PORT
CMD ["npm", "run", "start"]
