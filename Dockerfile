FROM python:3.11
WORKDIR /app
RUN pip install requests
COPY main.py .
EXPOSE 80
CMD ["/bin/bash", "-c", "python -u main.py & python -u -m http.server 80 --bind 0.0.0.0"]
