FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/
ENV UV_PYTHON_DOWNLOADS=0
WORKDIR /app
COPY . /app
RUN uv sync --locked
ENV OPENSSL_CONF=/app/src/ssl/openssl.cnf
# Run the application
ENTRYPOINT ["/app/.venv/bin/ledger-sync"]
