#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import request, make_response, render_template, redirect, session
from sites.admin.model import Banner


class StudentService(object):
    """
    api
    """

    def index(self):
        """
        :return:
        """
        records = Banner.query.filter(Banner.banner_type == 2, Banner.status == 100).all()
        html = ""
        for record in records[:5]:
            html += "<div><img src='{}' style='width:100%;height:100%'></div>".format(os.path.join("/layui", "temp", record.img_path))

        return render_template('student_home.html', html=html)

    def dispatch(self, func):
        """
        函数调度
        """
        map_func = {
            "index": self.index
        }
        if func in map_func:
            return map_func[func]()
