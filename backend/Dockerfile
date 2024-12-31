# Use Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure Poetry
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project true

# Install dependencies
RUN poetry install --no-root

# Copy application code
COPY . .

# Set default command to bash so container stays running
CMD ["bash"] 