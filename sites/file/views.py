#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from sites.file.file_api import FileService

file = Blueprint('file', __name__, url_prefix='/file')
file_service = FileService()


@file.route("<string:func>", methods=['GET', 'POST'])
def dispatch(func):
    """
    路由调度
    """
    return file_service.dispatch(func)
