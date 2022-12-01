ARG PY_VERSION=3.9

FROM amazon/aws-lambda-python:$PY_VERSION as install-stage

# Declare it a second time so it's brought into this scope.
ARG PY_VERSION=3.9

# Install the Python packages necessary to install the Lambda dependencies.
RUN python3 -m pip install --no-cache-dir \
    pip \
    setuptools \
    wheel \
  # This version of pipenv is the minimum version to allow passing arguments
  # to pip with the --extra-pip-args option.
  && python3 -m pip install --no-cache-dir "pipenv>=2022.9.8"

WORKDIR /tmp

# Copy in the dependency files.
COPY src/py$PY_VERSION/ .

# Install the Lambda dependencies.
#
# The --extra-pip-args option is used to pass necessary arguments to the
# underlying pip calls.
RUN pipenv sync --system --extra-pip-args="--no-cache-dir --target ${LAMBDA_TASK_ROOT}"

FROM amazon/aws-lambda-python:$PY_VERSION as build-stage

###
# For a list of pre-defined annotation keys and value types see:
# https://github.com/opencontainers/image-spec/blob/master/annotations.md
###
# github@cisa.dhs.gov is a very generic email distribution, and it is
# unlikely that anyone on that distribution is familiar with the
# particulars of your repository.  It is therefore *strongly*
# suggested that you use an email address here that is specific to the
# person or group that maintains this repository; for example:
# LABEL org.opencontainers.image.authors="vm-fusion-dev-group@trio.dhs.gov"
LABEL org.opencontainers.image.authors="github@cisa.dhs.gov"
LABEL org.opencontainers.image.vendor="Cybersecurity and Infrastructure Security Agency"

# Declare it a third time so it's brought into this scope.
ARG PY_VERSION=3.9

# This must be present in the image to generate a deployment artifact.
ENV BUILD_PY_VERSION=$PY_VERSION

COPY --from=install-stage ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy in the handler.
COPY src/lambda_handler.py .

# Ensure our handler is invoked when the image is used.
CMD ["lambda_handler.handler"]
