FROM node:20-alpine as build

WORKDIR /src

COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npm", "run", "dev"]


# FROM node:20 as build

# WORKDIR /src

# COPY ./package.json /src/package.json
# COPY ./package-lock.json /src/package-lock.json

# RUN npm install

# COPY . /src

# RUN npm run build
# RUN rm -rf ./node_modules

# FROM nginx:1.23-alpine
# WORKDIR /usr/share/nginx/html
# COPY /nginx.conf /etc/nginx
# RUN rm /etc/nginx/conf.d/default.conf
# COPY --from=build /src/dist/ /usr/share/nginx/html

# EXPOSE 80
# ENTRYPOINT ["nginx", "-g", "daemon off;"]