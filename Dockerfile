ARG PY_VERSION=3.9

FROM amazon/aws-lambda-python:$PY_VERSION

# Declare it a second time so it's brought into this scope.
ARG PY_VERSION=3.9
# Get the base output file name from the command line if provided.
ARG FILE_NAME=example

# For a list of pre-defined annotation keys and value types see:
# https://github.com/opencontainers/image-spec/blob/master/annotations.md
# Note: Additional labels are added by the build workflow.
LABEL org.opencontainers.image.authors="nicholas.mcdonnell@cisa.dhs.gov"
LABEL org.opencontainers.image.vendor="Cyber and Infrastructure Security Agency"

# Bring the command line ARGs into the environment so they are available
# in the built image.
ENV BUILD_PY_VERSION=$PY_VERSION
ENV BUILD_FILE_NAME=$FILE_NAME

WORKDIR /var/task
RUN mkdir build output
WORKDIR build

# We need the zip utility to create a deployment package archive.
RUN yum install -y zip

# Install the Python packages necessary to build a deployment package.
RUN python3 -m pip install --no-cache-dir --upgrade \
  pip \
  setuptools \
  wheel
RUN python3 -m pip install --no-cache-dir --upgrade pipenv

# Copy in the build files.
COPY src/build_artifact.sh build_artifact.sh
COPY src/lambda_handler.py lambda_handler.py
COPY src/py$PY_VERSION/ .

# Set up the application's Python virtualenv and verify.
RUN pipenv install --site-packages
RUN pipenv check

# Generate an deployment package artifact from the virtualenv.
ENTRYPOINT ["./build_artifact.sh"]
