FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR $PYSETUP_PATH

# Copy poetry configuration files
COPY pyproject.toml ./

# Install dependencies
RUN poetry install --no-root

# Copy the project
COPY . .

# Install the package
RUN poetry install

# Set entrypoint
ENTRYPOINT ["poetry", "run"]

# Default command
CMD ["python", "-m", "my_python_package"]
