"""Simple AWS Lambda handler to verify functionality."""

# Standard Python Libraries
from datetime import datetime, timezone
import logging
from typing import Any, Optional, Union

# Third-Party Libraries
import cowsay
import cowsay.characters

# cisagov Libraries
from example import example_div

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def failed_task(result: dict[str, Any], error_msg: str) -> None:
    """Update a given result because of a failure during processing."""
    result["success"] = False
    result["error_message"] = error_msg


def task_default(event):
    """Provide a result if no valid task was provided."""
    result = {}
    error_msg = 'Provided task "%s" is not supported.'

    task = event.get("task", None)
    logging.error(error_msg, task)
    failed_task(result, error_msg % task)

    return result


def task_cowsay(event) -> dict[str, Union[Optional[str], bool]]:
    """Generate an output message using the provided information."""
    result: dict[str, Union[Optional[str], bool]] = {"message": None, "success": True}

    character: str = event.get("character", "tux")
    if character not in cowsay.characters.CHARS.keys():
        error_msg = 'Character "%s" is not valid.'
        logging.error(error_msg, character)
        failed_task(result, error_msg % character)
    else:
        contents: str = event.get("contents", "Hello from AWS Lambda!")
        logger.info(
            'Creating output using "%s" with contents "%s"', character, contents
        )
        result["message"] = cowsay.get_output_string(character, contents)

    return result


def task_divide(event) -> dict[str, Union[Optional[float], bool]]:
    """Divide one number by another and provide the result."""
    result: dict[str, Union[Optional[float], bool]] = {"result": None, "success": True}
    numerator: str = event.get("numerator", None)
    denominator: str = event.get("denominator", None)

    if denominator is None or numerator is None:
        error_msg = "Request must include both a numerator and a denominator."
        logging.error(error_msg)
        failed_task(result, error_msg)
    else:
        try:
            variable_error_msg = "numerator: %s, denominator: %s"
            result["result"] = example_div(int(numerator), int(denominator))
        except ValueError:
            error_msg = "The provided values must be integers."
            logging.error(error_msg)
            logging.error(variable_error_msg, numerator, denominator)
            failed_task(result, error_msg)
        except ZeroDivisionError:
            error_msg = "The denominator cannot be zero."
            logging.error(error_msg)
            logging.error(variable_error_msg, numerator, denominator)
            failed_task(result, error_msg)

    return result


def handler(event, context) -> dict[str, Optional[str]]:
    """Process the event and generate a response.

    The event should have a task member that is one of the supported tasks.

    :param event: The event dict that contains the parameters sent when the function
                  is invoked.
    :param context: The context in which the function is called.
    :return: The result of the action.
    """
    response: dict[str, Optional[str]] = {"timestamp": str(datetime.now(timezone.utc))}

    task_name = f"task_{event.get('task')}"
    task = globals().get(task_name, task_default)

    result: dict[str, Any]
    if not callable(task):
        logging.error("Provided task is not a callable.")
        logging.error(task)
        result = task_default(event)
    else:
        result = task(event)

    response.update(result)
    return response
