# -*- coding: utf-8 -*-
# src/apytizer/media_types.py
"""Media types (previously MIME types) and subtypes.

.. _IANA:
    https://www.iana.org/assignments/media-types/media-types.xhtml

"""

# Standard Library Imports
from __future__ import annotations
import enum
import mimetypes
import re
from typing import Optional


@enum.unique
class MediaType(str, enum.Enum):
    """Implements media types."""

    @property
    def type(self) -> Optional[str]:
        """Content type."""
        match = re.match(r"[a-z]+(?=/)", self._value_)
        result = match.group(0) if match else None
        return result

    @property
    def subtype(self) -> Optional[str]:
        """Content subtype."""
        match = re.search(r"(?<=/)[a-z+-]+", self._value_)
        result = match.group(0) if match else None
        return result

    @property
    def extension(self) -> Optional[str]:
        """File extension."""
        result = mimetypes.guess_extension(self._value_)
        return result

    # application
    APPLICATION_JAVASCRIPT = "application/javascript"
    APPLICATION_JSON = "application/json"
    APPLICATION_MANIFEST = "application/manifest+json"
    APPLICATION_MSWORD = "application/msword"
    APPLICATION_OCTET_STREAM = "application/octet-stream"
    APPLICATION_ODA = "application/oda"
    APPLICATION_PDF = "application/pdf"
    APPLICATION_PKCS7_MIME = "application/pkcs7-mime"
    APPLICATION_POSTSCRIPT = "application/postscript"
    APPLICATION_RTF = "application/rtf"
    APPLICATION_RTX = "application/rtx"
    APPLICATION_SQL = "application/sql"
    APPLICATION_TAR = "application/x-tar"
    APPLICATION_XML = "application/xml"
    APPLICATION_ZIP = "application/zip"

    # audio
    AUDIO_AIFF = "audio/x-aiff"
    AUDIO_BASIC = "audio/basic"
    AUDIO_MP4 = "audio/mp4"
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_MIDI = "audio/midi"
    AUDIO_REALAUDIO = "audio/x-pn-realaudio"
    AUDIO_WAV = "audio/x-wav"

    # image
    IMAGE_BMP = "image/bmp"
    IMAGE_GIF = "image/gif"
    IMAGE_ICON = "image/vnd.microsoft.icon"
    IMAGE_IEF = "image/ief"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PICT = "image/pict"
    IMAGE_PNG = "image/png"
    IMAGE_RGB = "image/x-rgb"
    IMAGE_SVG = "image/svg+xml"
    IMAGE_TIFF = "image/tiff"

    # message
    MESSAGE_PARTIAL = "message/partial"
    MESSAGE_RFC822 = "message/rfc822"

    # multipart
    MULTIPART_BYTERANGES = "multipart/byteranges"
    MULTIPART_ENCRYPTED = "multipart/encrypted"
    MULTIPART_FORM_DATA = "multipart/form-data"
    MULTIPART_HEADER_SET = "multipart/header-set"
    MULTIPART_MULTILINGUAL = "multipart/multilingual"
    MULTIPART_SIGNED = "multipart/signed"

    # text
    TEXT_CSS = "text/css"
    TEXT_CSV = "text/csv"
    TEXT_DNS = "text/dns"
    TEXT_HTML = "text/html"
    TEXT_JAVASCRIPT = "text/javascript"
    TEXT_MARKDOWN = "text/markdown"
    TEXT_PLAIN = "text/plain"
    TEXT_PYTHON = "text/x-python"
    TEXT_RTF = "text/rtf"
    TEXT_RTX = "text/rtx"
    TEXT_SETEXT = "text/x-setext"
    TEXT_SGML = "text/x-sgml"
    TEXT_STRINGS = "text/strings"
    TEXT_TSV = "text/tab-separated-values"
    TEXT_VCARD = "text/x-vcard"
    TEXT_XML = "text/xml"

    # video
    VIDEO_H264 = "video/H264"
    VIDEO_MP4 = "video/mp4"
    VIDEO_MPEG = "video/mpeg"
    VIDEO_MSVIDEO = "video/x-msvideo"
    VIDEO_QUICKTIME = "video/quicktime"
    VIDEO_RAW = "video/raw"
    VIDEO_SGI_MOVIE = "video/x-sgi-movie"
    VIDEO_WEBM = "video/webm"
