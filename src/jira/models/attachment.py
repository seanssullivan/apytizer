# -*- coding: utf-8 -*-

# Standard Library Imports
import logging

# Local Imports
from ...base.model import BasicModel


class JiraAttachment(BasicModel):
    """
    Implements an instance of an attachment from Jira.
    """

    def __init__(self, data):
        super().__init__(data)
