FROM python:3.9
COPY src/ /app
COPY secrets/ /app/secrets
COPY example_config.json /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./bot.py