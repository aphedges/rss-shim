# syntax=docker/dockerfile:1

FROM python:3.13.12-alpine3.23

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -e . -c requirements-lock.txt

# Copy remaining files
COPY LICENSE .
COPY README.md .
COPY src/ src/

# Re-install so `pip` stores all metadata properly
RUN pip install --no-cache-dir --no-deps -e .

CMD ["/bin/sh", "-c", "python -u -m rss_shim"]
