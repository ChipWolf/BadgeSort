# BadgeSort Docker image
FROM duffn/python-poetry:3.11-slim

# Install system dependencies for PNG fallback support
RUN apt-get update && apt-get install -y \
    imagemagick \
    librsvg2-bin \
    && rm -rf /var/lib/apt/lists/*

# Set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY pyproject.toml poetry.lock ./
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install --no-root

WORKDIR /app
COPY . .

RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install

CMD ["/entrypoint.sh"]
