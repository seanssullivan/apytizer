# -*- coding: utf-8 -*-

# Standard Library Imports
from datetime import datetime
import dateutil
import logging
import re

# Local Imports
from ...base.model import BasicModel


class JiraAttachment(BasicModel):
    """
    Implements an instance of an attachment from Jira.
    """
    _properties = [
        'author',
        'content',
        'created',
        'filename',
        'id',
        'mimeType'
        'self',
        'size',
        'thumbnail'
    ]

    def __init__(self, data):
        super().__init__(self._validate_params(data))

    @classmethod
    def _validate_params(self, params):
        if not all(key in params.keys() for key in self._properties):
            missing_params = ' '.join([key for key in self._properties if key not in params.keys()])
            raise ValueError('missing required properties: {}'.format(missing_params))

        if isinstance(params.get('created'), str):
            params.update({'created': dateutil.parser.isoparse(params.get('created'))})

        if not re.fullmatch(r'^[\w,\s-]+\.[a-zA-Z]+$', params.get('filename')):
            raise ValueError('{} is not a valid filename'.format(params.get('filename')))

        if 'id' in params.keys() and not re.fullmatch(r'^\d+$', str(params.get('id'))):
            raise ValueError('invalid id')

        return {k: v for k, v in params if k in self._properties}
