# BadgeSort Docker image with WebP rasterization support
FROM duffn/python-poetry:3.11-slim

# Install system dependencies for WebP rasterization optimization
# - imagemagick: SVG to PNG conversion for 14x14px badge icons
# - webp: PNG to WebP conversion for ~78% size reduction vs compressed SVG
RUN apt-get update && apt-get install -y \
    imagemagick \
    webp \
    && rm -rf /var/lib/apt/lists/* \
    # Configure ImageMagick to allow SVG processing for badge icons
    && sed -i 's/<policy domain="coder" rights="none" pattern="SVG" \/>/<policy domain="coder" rights="read|write" pattern="SVG" \/>/' /etc/ImageMagick-6/policy.xml \
    || true

# Set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY pyproject.toml poetry.lock ./
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install --no-root

WORKDIR /app
COPY . .

RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install

CMD ["/entrypoint.sh"]
