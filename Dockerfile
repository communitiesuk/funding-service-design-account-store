FROM python:3.10-bullseye@sha256:9fb9e8177ab008b19ea53e4eb2a98de209f84195ce398f0daf3441f633c41148

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:92aa10fc236a5cbd3624c9909f855a860bd209fef17756c831ee84c478423517 /uv /uvx /bin/

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
