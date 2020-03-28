FROM python:3.6.10-alpine3.11
ENV LC_ALL C.UTF-8

WORKDIR /usr/src/app

COPY requirements.txt ask_bot.py ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "./ask_bot.py"]
