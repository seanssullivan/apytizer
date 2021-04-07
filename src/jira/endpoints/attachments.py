# -*- coding: utf-8 -*-

# Local Imports
from ...abstracts.api import AbstractAPI
from ...base.decorators import json_response
from ...base.endpoint import BasicEndpoint


class JiraAttachmentsEndpoint(BasicEndpoint):
    """
    Class for interacting with the Jira attachments API endpoint.
    """

    def __init__(self, api: AbstractAPI, headers: dict = None):
        super().__init__(self, api, path="attachment", headers=headers)

    def add(self, *args, **kwargs):
        """
        Attachments must be added directly to an issue.
        """
        raise NotImplementedError

    def all(self, *args, **kwargs):
        """
        Not able to retrieve multiple attachments from this endpoint.
        """
        raise NotImplementedError

    @json_response
    def get(self, ref: int or str, headers: dict = None):
        """
        Get attachment metadata from the Jira API endpoint.

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.

        Returns:
            Dictionary containing the metadata.

        """
        response = super().get(ref, headers)
        return response

    @json_response
    def settings(self, headers: dict = None):
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


class JiraExpandedAttachmentEndpoint:
    """
    Class for interacting with metadata for the contents of archive attachments.
    """

    def __init__(self, api: AbstractAPI, headers: dict = None):
        super().__init__(self, api, path="attachment", headers=headers)

    def add(self, *args, **kwargs):
        """
        Attachments must be added directly to an issue.
        """
        raise NotImplementedError

    def all(self, *args, **kwargs):
        """
        Not able to retrieve multiple attachments from this endpoint.
        """
        raise NotImplementedError

    @json_response
    def get(self, ref: int or str, expand: str, headers: dict = None):
        """
        Get attachment metadata from the Jira API endpoint.

        Args:
            ref: Issue ID or Key.
            expand: Specify whether to return metadata in either
                human-readable format or raw data.
            headers (optional):  Override endpoint- and API-level headers.

        Returns:
            Dictionary containing the metadata.

        """
        response = super().get(ref, headers)
        return response

    def update(self, *args, **kwargs):
        """
        Not able to update attachment contents.
        """
        raise NotImplementedError

    def remove(self, ref: int or str, headers: dict = None):
        """
        Not able to remove metadata for attachment contents.
        """
        raise NotImplementedError
