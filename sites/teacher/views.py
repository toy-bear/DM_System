#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from sites.teacher.teacher_api import TeacherService

teacher = Blueprint('teacher', __name__, url_prefix='/teacher')
teacher_service = TeacherService()


@teacher.route("<string:func>", methods=['GET', 'POST'])
def dispatch(func):
    """
    路由调度
    """
    return teacher_service.dispatch(func)
