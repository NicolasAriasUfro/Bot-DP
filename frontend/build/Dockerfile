FROM node:23-slim AS build
WORKDIR /app
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar el código fuente
COPY . .

# Ejecutar tests y solo continuar con el build si pasan
RUN npm test && npm run build-ntc

FROM nginx:alpine

# Copiar los archivos compilados desde la etapa de build
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080

# Corregir la ruta de default.conf (no se puede acceder a directorios padres)
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]