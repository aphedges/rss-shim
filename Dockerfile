FROM python:3.12.8-alpine3.20

WORKDIR /app

# Install dependencies
COPY requirements.txt .
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements.txt -c requirements-lock.txt

# Copy over and install application
COPY LICENSE .
COPY README.md .
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir --no-deps . -c requirements-lock.txt

CMD ["/bin/sh", "-c", "python -u -m rss_shim"]
