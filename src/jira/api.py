# -*- coding: utf-8 -*-

# Standard Library Imports
import logging

# Local Imports
from ..base.api import BasicAPI


class JiraAPI(BasicAPI):
    """
    Implements the API that makes it possible to interact with a JIRA account and its data.
    """

    def __init__(self, username: str, api_key: str):
        BasicAPI.__init__(
            self,
            auth=(username, api_key),
            headers={'Content-Type': 'application/json'}
        )
