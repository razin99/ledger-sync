FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

# Use the system Python across both stages
ENV UV_PYTHON_DOWNLOADS=0

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project --no-editable --no-dev

# Copy the project into the intermediate image
COPY . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-editable --no-dev

FROM python:3.14-slim

# Copy the environment, but not the source code
COPY --from=builder /app/.venv /app/.venv

ENV OPENSSL_CONF=/app/.venv/lib/python3.14/site-packages/ledger_sync/ssl/openssl.cnf
ENTRYPOINT ["/app/.venv/bin/ledger-sync"]
