# step 1
FROM node:16

# step 2
WORKDIR /usr/src/app

# step 3
COPY package*.json ./
RUN npm install

# step 4
COPY server.js .

# step 5
EXPOSE 8000

# step 6
CMD ["node", "server.js"]
