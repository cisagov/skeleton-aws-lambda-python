#!/usr/bin/env pytest -vs
"""Tests for the AWS Lambda Python skeleton project."""

# Standard Python Libraries
import json
import os

# Third-Party Libraries
import pytest

# cisagov Libraries
from cisagov_lambda import __version__, lambda_handler

GITHUB_RELEASE_TAG = os.getenv("GITHUB_RELEASE_TAG")
COWSAY_TUX_MESSAGE_LINES = [
    "  ______________________",
    "| Hello from AWS Lambda! |",
    "  ======================",
    "                           \\",
    "                            \\",
    "                             \\",
    "                              .--.",
    "                             |o_o |",
    "                             |:_/ |",
    "                            //   \\ \\",
    "                           (|     | )",
    "                          /'\\_   _/`\\",
    "                          \\___)=(___/",
]


def test_failed_task():
    """Test that a failed task result is correctly formatted."""
    result = {}
    test_message = "This is a pytest test message."
    lambda_handler.failed_task(result, test_message)

    assert len(result.keys()) == 2, "unexpected number of keys in the result"
    assert "success" in result.keys(), 'missing "success" key in the result'
    assert "error_message" in result.keys(), 'missing "error_message" key in the result'

    assert result["success"] is False, "incorrect success value"
    assert result["error_message"] == test_message, 'incorrect "error_message" value'


def test_task_default():
    """Test the functionality of the default task."""
    with open("events/default.json") as json_file:
        event = json.load(json_file)
    result = lambda_handler.task_default(event)

    assert len(result.keys()) == 2, "unexpected number of keys in the result"
    assert "success" in result.keys(), 'missing "success" key in the result'
    assert "error_message" in result.keys(), 'missing "error_message" key in the result'

    assert result["success"] is False, 'incorrect "success" value'
    assert (
        result["error_message"] == 'Provided task "None" is not supported.'
    ), 'incorrect "error_message" value'


def test_task_cowsay():
    """Test the functionality of the cowsay task."""
    with open("events/cowsay.json") as json_file:
        event = json.load(json_file)
    result = lambda_handler.task_cowsay(event)

    assert len(result.keys()) == 2, "unexpected number of keys in the result"
    assert "success" in result.keys(), 'missing "success" key in the result'
    assert "message" in result.keys(), 'missing "message" key in the result'

    assert result["success"] is True, 'incorrect "success" value'
    assert (
        result["message"].splitlines() == COWSAY_TUX_MESSAGE_LINES
    ), 'incorrect "message" value'


def test_divide_task():
    """Test the functionality of the divide task."""
    with open("events/divide.json") as json_file:
        event = json.load(json_file)
    result = lambda_handler.task_divide(event)

    assert len(result.keys()) == 2, "unexpected number of keys in the result"
    assert "success" in result.keys(), 'missing "success" key in the result'
    assert "result" in result.keys(), 'missing "message" key in the result'

    assert result["success"] is True, 'incorrect "success" value'
    assert result["result"] == 0.5, 'incorrect "result" value'


@pytest.mark.skipif(
    GITHUB_RELEASE_TAG in [None, ""],
    reason="this is not a release (GITHUB_RELEASE_TAG not set)",
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        GITHUB_RELEASE_TAG == f"v{__version__}"
    ), "GITHUB_RELEASE_TAG does not match the project version"
