FROM python:3.11-slim
WORKDIR /app
RUN pip install requests
COPY main.py .
CMD ["/bin/bash", "-c", "python -u main.py"]
