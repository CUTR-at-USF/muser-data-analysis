## Dockerfile
# Created by Ankit Raj
# Pulling from base Python image

FROM python:3.7-slim

# Author of file
LABEL maintainer="Ankit Raj"

# Set the working directory of the docker image
WORKDIR /muser-data-analysis
ADD . /muser-data-analysis

## Install native libraries, required for numpy
#RUN apk --no-cache add musl-dev linux-headers g++

# Upgrade pip
RUN pip install --upgrade pip

# Install packages listed in requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run.py"]