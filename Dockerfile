FROM python:3.10-bullseye@sha256:5c6f3a5a8ab7f559a2d5adb543030c0306e5656a049be19fe51b1677ca8d04d7

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:dc60491f42c9c7228fe2463f551af49a619ebcc9cbd10a470ced7ada63aa25d4 /uv /uvx /bin/

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "wsgi:app", "-b", "0.0.0.0:8080"]
