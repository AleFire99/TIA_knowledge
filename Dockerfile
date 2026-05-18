FROM python:3.12-slim AS builder
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir \
    mkdocs-material \
    mkdocs-static-i18n \
    mkdocs-awesome-pages-plugin \
    mkdocs-mermaid2-plugin
RUN mkdocs build --strict

FROM nginx:alpine
COPY --from=builder /app/site /usr/share/nginx/html
EXPOSE 80
