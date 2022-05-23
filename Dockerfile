FROM python:3.9-alpine3.13
LABEL maintainer="rjoaquinito"

ENV PYTHONUNBUFFERED 1

# Copy the requirements file from our local machine into the specified dir in the docker image
COPY ./requirements.txt /tmp/requirements.txt 
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy the app directory to the specified dir in the Docker container
COPY ./app /app
# Define this as the default directory where we run the commands
WORKDIR /app
# Expose port 8000 from our container to our machine
EXPOSE 8000

ARG DEV=false
# Command that is run when we build the image
RUN python -m venv /py && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [$DEV="true"]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Update the environment variable inside the image - add /py/bin
ENV PATH="/py/bin:$PATH"

# Switch to this user
USER django-user