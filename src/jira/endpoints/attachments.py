# -*- coding: utf-8 -*-

# Standard Library Imports
import logging

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
        super().__init__(self, api, path="attachment", headers=headers, methods=['GET', 'DELETE'])

    # def __getitem__(self, ref: int or str):
    #     """
    #     Returns a new endpoint with the appended reference.
    #     """
    #     endpoint = super().__getitem__(ref)
    #     endpoint.methods = self.methods
    #     return endpoint

    @json_response
    def get(self, ref: int or str, expand: str = None):
        """
        Get attachment metadata from the Jira API endpoint.

        Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/#api-rest-api-3-attachment-id-get

        Args:
            ref: Issue ID or Key.
            expand (optional): Specifies in which format to return the metadata.

        Returns:
            Dictionary containing the metadata.

        Raises:
            ValueError: Expand option has been provided but is not an accepted value.

        """
        headers = {'Accept': 'application/json'}

        if expand and expand in ('human', 'raw'):
            response = super().api.get(f'{ref!s}/expand/{expand}', headers)
        elif not expand:
            response = super().get(ref, headers=headers)
        else:
            raise ValueError(f"{expand} is not a valid option for 'expand'")

        return response

    def meta(self):
        """
        Get attachment settings from the Jira API endpoint.

        Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/#api-rest-api-3-attachment-meta-get

        Returns:
            Dictionary containing the settings.

        """
        response = super().api.get(f'{self.path!s}/meta', {'Accept': 'application/json'})
        return response

    def settings(self):
        """
        Alternative name for the meta() method.
        """
        return self.meta()

    def post(self, *args, **kwargs):
        """
        Attachments must be added directly to an issue.
        """
        raise NotImplementedError

    def put(self, *args, **kwargs):
        """
        Not able to update attachments.
        """
        raise NotImplementedError

    def delete(self, ref: int or str):
        """
        Delete an attachment from the Jira API endpoint.

        Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/#api-rest-api-3-attachment-id-delete

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.

        """
        response = super().delete(ref)
        return response
