FROM python:3.8-slim-buster
COPY ./src /app
WORKDIR /app


RUN adduser --system --no-create-home nonroot

RUN apt-get update
RUN apt-get install -y gcc libpq-dev

# Install dependencies
RUN pip3 install -r requirements.txt

# There are problem with grpcio version 1.37.0
# I din't find wich dependency cause this problem but installing 1.39.0 fixes the problem.
RUN pip3 install -r requirements_fix.txt

USER nonroot
CMD [ "python3", "exporter.py"]