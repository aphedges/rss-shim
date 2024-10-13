# `latest-dev` from 2024-10-13
FROM cgr.dev/chainguard/python@sha256:370b677f44814fe8dda63e9bb407af8fbd1fc147176808f0e5576100f67dbf73 AS builder

WORKDIR /app
# Temporary workaround
USER root

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy over and install application
COPY LICENSE .
COPY README.md .
COPY pyproject.toml .
COPY src/ src/

RUN pip install --user --no-cache-dir --no-deps .

# `latest` from 2024-10-13
FROM cgr.dev/chainguard/python@sha256:14b01460efdfb42b298cbb31807ed235d2661bfe576b849fce59614818302301 AS runner

WORKDIR /app
# Temporary workaround
USER root

COPY --from=builder /root/.local/lib/python3.12/site-packages /root/.local/lib/python3.12/site-packages
ENTRYPOINT ["python", "-u", "-m", "rss_shim"]

