#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of the web2py Web Framework
Copyrighted by Massimo Di Pierro <mdipierro@cs.depaul.edu>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)


Web2Py framework modules
========================
"""

__all__ = ['A', 'B', 'BEAUTIFY', 'BODY', 'BR', 'CENTER', 'CLEANUP', 'CODE', 'CRYPT', 'DAL', 'DIV', 'EM', 'EMBED', 'FIELDSET', 'FORM', 'Field', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HEAD', 'HR', 'HTML', 'HTTP', 'I', 'IFRAME', 'IMG', 'INPUT', 'IS_ALPHANUMERIC', 'IS_DATE', 'IS_DATETIME', 'IS_DATETIME_IN_RANGE', 'IS_DATE_IN_RANGE', 'IS_DECIMAL_IN_RANGE', 'IS_EMAIL', 'IS_EMPTY_OR', 'IS_EQUAL_TO', 'IS_EXPR', 'IS_FLOAT_IN_RANGE', 'IS_IMAGE', 'IS_INT_IN_RANGE', 'IS_IN_DB', 'IS_IN_SET', 'IS_IPV4', 'IS_LENGTH', 'IS_LIST_OF', 'IS_LOWER', 'IS_MATCH', 'IS_NOT_EMPTY', 'IS_NOT_IN_DB', 'IS_NULL_OR', 'IS_SLUG', 'IS_STRONG', 'IS_TIME', 'IS_UPLOAD_FILENAME', 'IS_UPPER', 'IS_URL', 'LABEL', 'LEGEND', 'LI', 'LINK', 'MARKMIN', 'MENU', 'META', 'OBJECT', 'OL', 'ON', 'OPTGROUP', 'OPTION', 'P', 'PRE', 'SCRIPT', 'SELECT', 'SPAN', 'SQLFORM', 'SQLTABLE', 'STYLE', 'TABLE', 'TAG', 'TBODY', 'TD', 'TEXTAREA', 'TFOOT', 'TH', 'THEAD', 'TITLE', 'TR', 'TT', 'UL', 'URL', 'XHTML', 'XML','redirect','current','embed64']

from globals import current
from html import *
from validators import *
from http import redirect, HTTP
from dal import DAL, Field
from sqlhtml import SQLFORM, SQLTABLE

