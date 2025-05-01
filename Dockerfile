FROM python:3.12-slim

# working dir
WORKDIR /bot

# install dependencies
RUN apt-get update && apt-get upgrade
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "cord.py"]
