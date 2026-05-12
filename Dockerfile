FROM python:3.13.0

## set the working directory
WORKDIR /app

## copy requirements.txt file to the dest
COPY requirements.txt .

## install the packages
RUN pip install --no-cache-dir -r requirements.txt

## copy source destination
COPY . .

EXPOSE 8000

ENTRYPOINT [ "fastapi", "run", "--port" , "8000" ]