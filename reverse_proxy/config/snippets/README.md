
## NGINX snippet files

These snippets can add dynamic behaviour to the reverse proxy based on the environment as well as being general-purpose reusable pieces of code.

They can be injected into the `nginx.conf` file by using the `include` directive.

Don't forget to add the following lines to the Dockerfile as to copy these snippets to the NGINX containing image.

```
# Copy local snippets to the snippets directory
COPY /config/snippets /etc/nginx/snippets
```
