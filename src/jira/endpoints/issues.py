# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Local Imports
from ...abstracts.api import AbstractAPI
from ...base.endpoint import BasicEndpoint
from ...base.decorators import json_response


log = logging.getLogger(__name__)


class JiraIssuesEndpoint(BasicEndpoint):
    """
    Class for interacting with the Jira issues API endpoint.

        - Create issue:                POST /rest/api/3/issue
        - Bulk create issue:           POST /rest/api/3/issue/bulk
        - Get create issue metadata:   GET /rest/api/3/issue/createmeta
        - Get issue:                   GET /rest/api/3/issue/{issueIdOrKey}
        - Edit issue:                  PUT /rest/api/3/issue/{issueIdOrKey}
        - Delete issue:                DELETE /rest/api/3/issue/{issueIdOrKey}
        - Assign Issue:                PUT /rest/api/3/issue/{issueIdOrKey}/assignee
        - Get change logs:             GET /rest/api/3/issue/{issueIdOrKey}/changelog
        - Get edit issue metadata:     GET /rest/api/3/issue/{issueIdOrKey}/editmeta
        - Send notification for issue: POST /rest/api/3/issue/{issueIdOrKey}/notify
        - Get transitions:             GET /rest/api/3/issue/{issueIdOrKey}/transitions

    """

    def __init__(self, api: AbstractAPI, headers: dict = None):
        super().__init__(self, api, path="issue", headers=headers)

    def add(self, data: dict or list, headers: dict = None, **kwargs):
        """
        Create issue(s) with Jira REST API.
        """
        if isinstance(data, dict):
            response = super().add(data, headers)
        elif isinstance(data, list):
            response = super().api.post(f'{self.url}/bulk', headers=headers, data={"issueUpdates": data})
        else:
            raise TypeError

        return response

    def all(self, *args, **kwargs):
        """
        Retrieving all issues is not possible at this endpoint.
        Use search() instead to retrieve mutliple issues.
        """
        raise NotImplementedError

    @json_response
    def get(self, ref: int or str, headers: dict = None, **kwargs):
        """
        Get issue from Jira API endpoint.

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.

        Returns:
            Dictionary containing the issue data.

        """
        response = super().get(ref, headers)
        return response

    def update(self, *args, **kwargs):
        """
        Not able to update attachments.
        """
        raise NotImplementedError

    def remove(self, ref: int or str, headers: dict = None, **kwargs):
        """
        Delete attachment from Jira API endpoint.

        Args:
            ref: Issue ID or Key.
            headers (optional):  Override endpoint- and API-level headers.

        """
        response = super().remove(ref, headers)
        return response
