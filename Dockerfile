# Using lightweight alpine image
FROM python:3.4-alpine

MAINTAINER mcourtney02124@gmail.com

# Installing packages
RUN apk update
RUN pip3 install --no-cache-dir pipenv

ENV PATH=$PATH:/usr/src/app/

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY src ./src

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 5000
#ENTRYPOINT ["/usr/src/app/bootstrap.sh"]

CMD sh /usr/src/app/bootstrap.sh

