FROM ghcr.io/astral-sh/uv:0.7.5 AS uv

FROM python:3.13.3 AS build-stage

WORKDIR /bot

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --compile-bytecode --no-install-project --no-editable

FROM python:3.13.3-slim

WORKDIR /bot

COPY --from=build-stage /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "/bot/main.py"]
