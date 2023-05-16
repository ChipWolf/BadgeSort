FROM duffn/python-poetry:3.9-bullseye

# Set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY pyproject.toml poetry.lock ./
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install --no-root

WORKDIR /app
COPY . .

RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install

CMD ["/entrypoint.sh"]
