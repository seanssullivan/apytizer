# -*- coding: utf-8 -*-

# Standard Library Imports
import logging

# Local Imports
from ..base.api import BasicAPI
from ..base.decorators import json_response


class JiraAPI(BasicAPI):
    """
    Implements the API that makes it possible to interact with a Jira account and its data.
    """

    def __init__(self, url: str, username: str, api_key: str):
        super().__init__(
            url=url,
            auth=(username, api_key),
            headers={'Content-Type': 'application/json'}
        )
