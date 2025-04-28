FROM node:18-slim AS build
WORKDIR /
COPY . .

RUN npm install

RUN npm run build


FROM nginx:alpine

COPY --from=build dist /usr/share/nginx/html

EXPOSE 8080
COPY ../default.conf /etc/nginx/conf.d/default.conf

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]