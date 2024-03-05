#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime
from sites import db

from flask import request, make_response, render_template, redirect, session
from sites.user.model import User
from sites.admin.model import Banner


class TeacherService(object):
    """
    api
    """

    def index(self):
        """
        :return:
        """
        records=Banner.query.filter(Banner.banner_type==1,Banner.status==100).all()
        html=""
        for record in records[:5]:
            html+="<div><img src='{}'></div>".format(os.path.join("/layui", "temp",  record.img_path))

        return render_template('teacher_home.html',html=html)

    def dispatch(self, func):
        """
        函数调度
        """
        map_func = {
            "index": self.index
        }
        if func in map_func:
            return map_func[func]()
