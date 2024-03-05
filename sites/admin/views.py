#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from sites.admin.admin_api import AdminService

admin = Blueprint('admin', __name__, url_prefix='/admin')
admin_service = AdminService()


@admin.route("<string:func>", methods=['GET', 'POST'])
def dispatch(func):
    """
    路由调度
    """
    return admin_service.dispatch(func)
