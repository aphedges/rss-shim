FROM python:3.11-slim
WORKDIR /app
COPY LICENSE README.md pyproject.toml setup.cfg setup.py ./
RUN pip install .
COPY src/ src/
RUN pip install .
CMD ["/bin/bash", "-c", "python -u -m rss_shim"]
