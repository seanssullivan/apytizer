# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Local Imports
from ...abstracts.api import AbstractAPI
from ...base.endpoint import BasicEndpoint
from ...base.decorators import json_response


class JiraIssuesEndpoint(BasicEndpoint):
    """
    Class for interacting with the Jira issues API endpoint.
    """

    def __init__(self, api: AbstractAPI, headers: dict = None):
        super().__init__(self, api, path="issue", headers=headers)

    def add(self, data: dict, headers: dict = None):
        """
        """
        response = super().add(data, headers)
        return response

    def all(self, *args, **kwargs):
        """
        Retrieving all issues is not possible at this endpoint.
        Use search() instead to retrieve a filtered subset of issues.
        """
        raise NotImplementedError

    @json_response
    def get(self, ref: int or str, headers: dict = None):
        """
        Get an issue from the Jira API endpoint.

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.

        Returns:
            Dictionary containing the issue data.

        """
        response = super().get(ref, headers)
        return response

    @json_response
    def transitions(self, headers: dict = None):
        """
        Get attachment settings from the Jira API endpoint.

        Args:
            headers (optional):  Override endpoint- and API-level headers.

        Returns:
            Dictionary containing the settings.

        """
        response = super().api.get(f'{self.path}/meta', headers)
        return response

    def update(self, *args, **kwargs):
        """
        Not able to update attachments.
        """
        raise NotImplementedError

    def remove(self, ref: int or str, headers: dict = None):
        """
        Delete an attachment from the Jira API endpoint.

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.

        """
        response = super().remove(ref, headers)
        return response
