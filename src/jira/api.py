# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Local Imports
from ..base.api import BasicAPI


log = logging.getLogger(__name__)


class JiraAPI(BasicAPI):
    """
    Implements the API that makes it possible to interact with a Jira account and its data.
    """

    def __init__(self, url: str, username: str, api_key: str, version: int = 3):
        super().__init__(
            url=urljoin(url, f'/rest/api/{version}'),
            auth=(username, api_key),
            headers={'Content-Type': 'application/json'}
        )
