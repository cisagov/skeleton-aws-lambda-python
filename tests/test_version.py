#!/usr/bin/env pytest -vs
"""Version tests for AWS Lambda Python skeleton project."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest

# cisagov Libraries
import cisagov_lambda

GITHUB_RELEASE_TAG = os.getenv("GITHUB_RELEASE_TAG")


@pytest.mark.skipif(
    GITHUB_RELEASE_TAG in [None, ""],
    reason="this is not a release (GITHUB_RELEASE_TAG not set)",
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        GITHUB_RELEASE_TAG == f"v{cisagov_lambda.__version__}"
    ), "GITHUB_RELEASE_TAG does not match the project version"
