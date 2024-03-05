#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from sites.user.user_api import UserService

user = Blueprint('user', __name__, url_prefix='/user')
user_service = UserService()


@user.route("<string:func>", methods=['GET', 'POST'])
def dispatch(func):
    """
    路由调度
    """
    return user_service.dispatch(func)
