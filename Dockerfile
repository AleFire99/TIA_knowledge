FROM python:3.12-slim AS builder
WORKDIR /app

# Trust any locally-added root CAs (e.g. a corporate proxy or antivirus TLS
# inspection cert) dropped into certs/ on the host — see certs/README.md.
# Empty on machines that don't need it; update-ca-certificates just no-ops.
COPY certs/ /usr/local/share/ca-certificates/
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt

COPY . .
RUN pip install --no-cache-dir zensical
RUN zensical build --config-file zensical.it.toml --strict
RUN zensical build --config-file zensical.en.toml --strict

FROM nginx:alpine
COPY --from=builder /app/site/it /usr/share/nginx/html/it
COPY --from=builder /app/site/en /usr/share/nginx/html/en
RUN printf '<!DOCTYPE html><meta http-equiv="refresh" content="0; url=/it/">' \
    > /usr/share/nginx/html/index.html
EXPOSE 80
