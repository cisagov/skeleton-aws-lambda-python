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
LABEL org.opencontainers.image.vendor="Cybersecurity and Infrastructure Security Agency"

# Bring the command line ARGs into the environment so they are available
# in the built image.
ENV BUILD_PY_VERSION=$PY_VERSION
ENV BUILD_FILE_NAME=$FILE_NAME

WORKDIR ${LAMBDA_TASK_ROOT}
RUN mkdir build output

# We need the zip utility to create a deployment package archive.
RUN yum update --assumeyes \
  && yum install --assumeyes zip \
  && yum clean all

# Install the Python packages necessary to build a deployment package.
RUN python3 -m pip install --no-cache-dir \
    pip \
    setuptools \
    wheel \
  && python3 -m pip install --no-cache-dir pipenv

# Copy in the build files.
COPY src/build_artifact.sh build
COPY src/py$PY_VERSION/ build
COPY src/lambda_handler.py .

# Get a pip-friendly requirements file from our managed Pipfile.
WORKDIR ${LAMBDA_TASK_ROOT}/build
RUN pipenv requirements --hash > requirements.txt

# Install the Lambda's requirements into the task root directory.
WORKDIR ${LAMBDA_TASK_ROOT}
RUN python3 -m pip install --no-cache-dir \
  --target . \
  --requirement build/requirements.txt

# Start with our handler.
CMD ["lambda_handler.handler"]
