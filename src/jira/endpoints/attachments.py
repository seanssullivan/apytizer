# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Local Imports
from ...abstracts.api import AbstractAPI
from ...base.endpoint import BasicEndpoint
from ...base.decorators import json_response


log = logging.getLogger(__name__)


class JiraAttachmentsEndpoint(BasicEndpoint):
    """
    Class for interacting with the Jira attachments API endpoint.

    Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments
    """

    def __init__(self, api: AbstractAPI, headers: dict = None):
        super().__init__(self, api, path="attachment", headers=headers)

    def add(self, *args, **kwargs):
        """
        Attachments must be added directly to an issue.
        """
        raise NotImplementedError

    @json_response
    def get(self, ref: int or str, headers: dict = None, **kwargs):
        """
        Get attachment metadata from the Jira API endpoint.
        Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/#api-rest-api-3-attachment-id-get

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.
            options (optional): Accepts an 'expand' parameter which specifies
                in which format to return the metadata.

        Returns:
            Dictionary containing the metadata.

        Raises:
            ValueError: Expand option has been provided but is not an accepted value.

        """
        expand = kwargs.get('expand')
        if expand and expand in ('human', 'raw'):
            url = urljoin(f'{ref!s}/expand/{expand}')
            response = super().api.get(url, headers)
        elif not expand:
            response = super().get(ref, headers)
        else:
            raise ValueError(f"{expand} is not a valid option for 'expand'")

        return response

    @json_response
    def meta(self, headers: dict = None, **kwargs):
        """
        Get attachment settings from the Jira API endpoint.
        Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/#api-rest-api-3-attachment-meta-get

        Args:
            headers (optional):  Override endpoint- and API-level headers.

        Returns:
            Dictionary containing the settings.

        """
        url = urljoin(self.path, 'meta')
        response = super().api.get(url, headers)
        return response

    def settings(self, headers: dict = None, **kwargs):
        """
        Alternative name for the meta() method.
        """
        return self.meta(headers, **kwargs)

    def update(self, *args, **kwargs):
        """
        Not able to update attachments.
        """
        raise NotImplementedError

    def remove(self, ref: int or str, headers: dict = None, **kwargs):
        """
        Delete an attachment from the Jira API endpoint.
        Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/#api-rest-api-3-attachment-id-delete

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.

        """
        response = super().remove(ref, headers)
        return response
