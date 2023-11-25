# `latest-dev` from 2023-11-06
FROM cgr.dev/chainguard/python@sha256:797905aeb2254a1fd6d328a104cdc6cb95eb6ccee53261a98cdbac1ca498bdf8 as builder
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
COPY setup.cfg .
COPY setup.py .
COPY src/ src/
RUN pip install --user --no-cache-dir --no-deps .

# `latest` from 2023-11-06
FROM cgr.dev/chainguard/python@sha256:14b01460efdfb42b298cbb31807ed235d2661bfe576b849fce59614818302301
WORKDIR /app
# Temporary workaround
USER root

COPY --from=builder /root/.local/lib/python3.12/site-packages /root/.local/lib/python3.12/site-packages
ENTRYPOINT ["python", "-u", "-m", "rss_shim"]
