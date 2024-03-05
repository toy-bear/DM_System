#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime
from sites import db
from flask import request, make_response, render_template, redirect, session
from sites.admin.model import Banner


class AdminService(object):
    """
    api
    """

    def banner_list(self):
        """
        列表
        :return:
        """
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        records = Banner.query.filter()
        total = records.count()
        result = []
        for record in records[(page - 1) * limit:page * limit]:
            banner_type = "教师" if record.banner_type == 1 else "学生"
            status = "启用" if record.status == 100 else "禁用"
            result.append({
                "id": str(record.id),
                "file": record.img_path,
                "banner_type": banner_type,
                "status": status,
                "update_time": record.update_time,
                "create_time": record.create_time,
            })
        return make_response({"code": 0, "data": result, "count": total})

    def banner_add(self):
        file_name = request.args.get('file_name')
        banner_type = request.args.get('banner_type')
        status = request.args.get('status')
        status = 100 if status == "on" else -100
        record = Banner()
        record.img_path = file_name
        record.banner_type = banner_type
        record.status = status
        record.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(record)
        db.session.commit()

        return make_response((
            json.dumps({"status": 10000, "msg": "成功"}),
            200,
            {'Content-Type': 'application/json; charset=utf-8'}
        ))

    def banner_edit(self):
        file_name = request.args.get('file_name')
        banner_type = request.args.get('banner_type')
        status = request.args.get('status')
        status = 100 if status == "on" else -100
        banner_id = request.args.get('id')
        record = Banner.query.filter(Banner.id == banner_id).first()
        record.status = status
        record.banner_type = banner_type
        record.img_path = file_name
        record.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(record)
        db.session.commit()
        return make_response((
            json.dumps({"status": 10000, "msg": "成功"}),
            200,
            {'Content-Type': 'application/json; charset=utf-8'}
        ))

    def banner_delete(self):
        _id = request.args.get('id')
        Banner.query.filter(Banner.id == _id).delete()
        db.session.commit()
        return make_response((
            json.dumps({"status": 10000, "msg": "成功"}),
            200,
            {'Content-Type': 'application/json; charset=utf-8'}
        ))

    def banner_get(self):
        _id = request.args.get('id')
        record = Banner.query.filter(Banner.id == _id).first()
        result = {
            "id": record.id,
            "img_path":os.path.join("/layui", "temp",  record.img_path),
            "file_name":record.img_path,
            "banner_type": str(record.banner_type),
            "status": record.status
        }
        return make_response({"code": 0, "data": result})

    def dispatch(self, func):
        """
        函数调度
        """
        map_func = {
            "banner_list": self.banner_list,
            "banner_add": self.banner_add,
            "banner_get": self.banner_get,
            "banner_edit": self.banner_edit,
            "banner_delete": self.banner_delete,
            "banner": self.banner,
            "index": self.index,
            "upload": self.upload,
            "banner_edit_page": self.banner_edit_page
        }
        if func in map_func:
            return map_func[func]()

    def banner_edit_page(self):
        _id = request.args.get('id')
        return render_template('banner_add.html', id=_id)

    def upload_resource_file(self, storage):
        """
        上传文件并且保存
        :param storage:
        :return:
        """
        file_data = storage.read()
        file_name = storage.filename
        file_type = file_name.split('.')[-1]

        save_path = os.path.join(os.path.abspath('templates'), "layui", "temp", storage.filename)
        if file_type not in ['jpg', 'png']:
            return
        with open(save_path, 'wb') as w:
            w.write(file_data)
        return save_path, storage.filename

    def upload(self):
        """
        上传文件
        :return:
        """
        for _, storage in request.files.items():
            file_path, file_name = self.upload_resource_file(storage)
            if not file_path:
                return make_response((
                    json.dumps({"status": 10001, "msg": "文件类型不正确"}),
                    200,
                    {'Content-Type': 'application/json; charset=utf-8'}
                ))
            return make_response((
                json.dumps({"status": 10000, "file_name": file_name}),
                200,
                {'Content-Type': 'application/json; charset=utf-8'}
            ))

    def banner(self):
        """
        :return:
        """
        return render_template('banner.html')

    def index(self):
        """
        :return:
        """
        return render_template('admin_home.html')
