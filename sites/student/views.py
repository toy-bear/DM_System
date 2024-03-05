#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from sites.student.student_api import StudentService

student = Blueprint('student', __name__, url_prefix='/student')
student_service = StudentService()


@student.route("<string:func>", methods=['GET', 'POST'])
def dispatch(func):
    """
    路由调度
    """
    return student_service.dispatch(func)
