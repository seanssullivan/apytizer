# -*- coding: utf-8 -*-

# Local Imports
from ...abstracts.api import AbstractAPI
from ...base.endpoint import BasicEndpoint
from ...base.decorators import json_response


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
    def get(self, ref: int or str, headers: dict = None, options: dict = None):
        """
        Get attachment metadata from the Jira API endpoint.

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
        expand = options.get('expand')
        if expand and expand in ('human', 'raw'):
            response = super().api.get(f'{self.url}/{ref!s}/expand/{expand}', headers)
        elif not expand:
            response = super().get(ref, headers)
        else:
            raise ValueError(f"{expand} is not a valid option for 'expand'")

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
