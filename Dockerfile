FROM python:3.8-slim-buster

VOLUME ["/app"]

# Define working directory
WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY comment_generator /app/comment_generator
COPY test /app/test
COPY config.yaml /app/config.yaml
COPY run_server.py /app/run_server.py
COPY main.py /app/main.py

RUN pip3 install torch==1.8.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

EXPOSE 8080


CMD ["uvicorn", "run_server:app", "--host", "0.0.0.0", "--port", "8080"]