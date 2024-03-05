#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from sites.open_file.file_api import OpenFileService

open_file = Blueprint('open_file', __name__, url_prefix='/open_file')
open_file_service = OpenFileService()


@open_file.route("<string:func>", methods=['GET', 'POST'])
def dispatch(func):
    """
    路由调度
    """
    return open_file_service.dispatch(func)
