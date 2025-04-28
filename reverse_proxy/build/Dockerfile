# Use nginx for serving the built app
FROM nginx:alpine

# Copy the nginx configuration file
COPY /config/nginx.conf /etc/nginx/nginx.conf

# Copy local snippets to the snippets directory
COPY /config/snippets /etc/nginx/snippets

EXPOSE 8080

CMD ["nginx","-g", "daemon off;"]