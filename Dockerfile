FROM python:3.9.13-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt .
COPY . .

# install dependencies
RUN apt-get update
RUN pip install -r requirements.txt
# RUN python -m nltk.downloader punkt


# tell the port number container should expose
EXPOSE 8000

# run command 
CMD ["bash", "start.sh"]