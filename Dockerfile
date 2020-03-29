FROM python:3.6.10
ENV LC_ALL C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install cryptography \
    && apt-get purge -y --auto-remove gcc

WORKDIR /usr/src/app

COPY requirements.txt ask_bot.py ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "./ask_bot.py"]
