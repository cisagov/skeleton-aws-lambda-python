#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

ARTIFACT_FILE_NAME="${BUILD_FILE_NAME:-lambda-package.zip}"

output_directory="${LAMBDA_TASK_ROOT}/output"
artifact_path="$output_directory/$ARTIFACT_FILE_NAME"

# Build the deployment package by zipping the libraries and handler. We
# explicitly exclude the build/ and output/ subdirectories as they are
# not part of the deployment package.
cd "${LAMBDA_TASK_ROOT}" && zip -rq9 "$artifact_path" . -x "build/*" -x "output/*"
