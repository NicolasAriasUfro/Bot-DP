FROM node:23-slim AS build
WORKDIR /app
COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build-ntc


FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
COPY ../default.conf /etc/nginx/conf.d/default.conf

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]