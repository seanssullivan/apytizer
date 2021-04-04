# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import logging
import time

# Third-Party Imports
import requests


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)


def confirm_response(func):
    """
    Confirms successful API response.
    """
    @functools.wraps(func)
    def request_wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, timeout=self._timeout_after, **kwargs)
            response.raise_for_status()

        except requests.exceptions.ConnectionError as error:
            logging.debug("connection error")
            logging.info(f"Error message: {error}")
            return error

        except requests.exceptions.Timeout as error:
            logging.debug("request timed out")
            logging.info(f"Error message: {error}")
            return error

        else:
            logging.debug("response received")
            logging.info(f"Status code: {response.status_code}")
            return response

    return request_wrapper


def json_response(func):
    @functools.wraps(func)
    def request_wrapper(self, *args, **kwargs):
        response = func(self, *args, **kwargs)

        try:
            parsed_json = response.json()

        except ValueError:
            logging.debug("response not json format")
            return response.text

        else:
            logging.debug("received json response")
            return parsed_json

    return request_wrapper


def rate_limited(func):
    """
    Enforces a rate limit on API requests.
    """
    @functools.wraps(func)
    def limit_wrapper(self, *args, **kwargs):
        # Determine amount of time since previous request.
        time_since = time.time() - self._time_of_previous_request

        # Pause request if not enough time has passed.
        if time_since < self._wait_between_requests:
            logging.warning("rate limit reached")

            pause = self._wait_between_requests - time_since
            logging.info(f"waiting {pause!s} seconds")

            time.sleep(pause)

        # Send request to API.
        response = func(self, *args, **kwargs)

        # Set time of previous request.
        self._time_of_previous_request = time.time()

        return response

    return limit_wrapper
