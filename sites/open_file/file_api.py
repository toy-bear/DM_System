#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime
import time

from sites import db

from flask import request, make_response, render_template, redirect, session, send_file
from sites.file.model import File
from sites.user.model import User


class OpenFileService(object):
    """
    api
    """

    def list(self):
        """
        列表
        :return:
        """
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        records = File.query.filter(File.private == 2)
        total = records.count()
        result = []
        can = 1
        for record in records[(page - 1) * limit:page * limit]:
            if record.can_view_operator and session['user_type'] != 1:
                can_view_operator = record.can_view_operator.split(',')
                user_id = str(session['user_id'])
                if user_id not in can_view_operator:
                    can = 0
            result.append({
                "id": str(record.id),
                "file_name": record.file_name,
                "operator": record.operator,
                "update_time": record.update_time,
                "create_time": record.create_time,
                "can": can
            })
        return make_response({"code": 0, "data": result, "count": total})

    def add(self):
        file_path = request.json.get('file_path')
        file_name = request.json.get('file_name')
        if not file_name:
            return make_response((
                json.dumps({"status": 10001, "msg": "文件必传"}),
                200,
                {'Content-Type': 'application/json; charset=utf-8'}
            ))
        data = request.json.get('data', [])
        record = File()
        record.file_path = file_path
        record.file_name = file_name
        record.file_type = file_name.split('.')[-1]
        operator = session['user']
        record.operator = operator
        record.private = 2
        record.private_file_path = 'output.jpg'
        can_view_operator = ''
        if data:
            can_view_operator = ",".join([str(i.get('value')) for i in data])
        record.can_view_operator = can_view_operator
        record.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(record)
        db.session.commit()

        return make_response((
            json.dumps({"status": 10000, "msg": "成功"}),
            200,
            {'Content-Type': 'application/json; charset=utf-8'}
        ))

    def edit(self):
        file_path = request.json.get('file_path')
        file_name = request.json.get('file_name')
        if not file_name:
            return make_response((
                json.dumps({"status": 10001, "msg": "文件必传"}),
                200,
                {'Content-Type': 'application/json; charset=utf-8'}
            ))
        data = request.json.get('data', [])
        _id = request.json.get('id')
        record = File.query.filter(File.id == _id).first()
        record.file_path = file_path
        record.file_name = file_name
        record.file_type = file_name.split('.')[-1]
        # todo

        record.private_file_path = '1.jpg'
        can_view_operator = ''
        if data:
            can_view_operator = ",".join([str(i.get('value')) for i in data])
        record.can_view_operator = can_view_operator
        record.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(record)
        db.session.commit()
        return make_response((
            json.dumps({"status": 10000, "msg": "成功"}),
            200,
            {'Content-Type': 'application/json; charset=utf-8'}
        ))

    def delete(self):
        _id = request.args.get('id')
        File.query.filter(File.id == _id).delete()
        db.session.commit()
        return make_response((
            json.dumps({"status": 10000, "msg": "成功"}),
            200,
            {'Content-Type': 'application/json; charset=utf-8'}
        ))

    def get(self):
        _id = request.args.get('id')
        record = File.query.filter(File.id == _id).first()
        result = {
            "id": record.id,
            "file_path": record.file_path,
            "file_name": record.file_name,
        }
        return make_response({"code": 0, "data": result})

    def down(self):
        _id = request.args.get('id')
        record = File.query.filter(File.id == _id).first()
        file_path = os.path.join(os.path.abspath('templates'), 'layui', "temp", record.file_path)
        if record.can_view_operator and session['user_type'] != 1:
            can_view_operator = record.can_view_operator.split(',')
            user_id = str(session['user_id'])
            if user_id not in can_view_operator:
                file_path = os.path.join(os.path.abspath('templates'), 'layui', "temp", record.private_file_path)

        return make_response(
            send_file(file_path,
                      as_attachment=True,
                      download_name=record.file_name))

    def dispatch(self, func):
        """
        函数调度
        """
        map_func = {
            "list": self.list,
            "add": self.add,
            "get": self.get,
            "edit": self.edit,
            "delete": self.delete,
            "index": self.index,
            "upload": self.upload,
            "edit_page": self.edit_page,
            "down": self.down
        }
        if func in map_func:
            return map_func[func]()

    def edit_page(self):
        _id = request.args.get('id')
        args = [User.user_type != 1]
        records = User.query.filter(*args).all()
        data = []
        file = File.query.filter(File.id == _id).first()
        for record in records:
            user_type = "教师" if record.user_type == 2 else "学生"
            data.append({
                "value": record.id,
                "title": record.user_name + "({})".format(user_type)
            })
        if file:
            value = file.can_view_operator.split(',')
        else:
            value = []

        return render_template('open_file_edit.html', id=_id, data=data, value=value)

    def upload_resource_file(self, storage):
        """
        上传文件并且保存
        :param storage:
        :return:
        """
        file_data = storage.read()
        file_path = str(int(time.time())) + storage.filename

        save_path = os.path.join(os.path.abspath('templates'), "layui", "temp", file_path)
        with open(save_path, 'wb') as w:
            w.write(file_data)
        return save_path, storage.filename, file_path

    def upload(self):
        """
        上传文件
        :return:
        """
        for _, storage in request.files.items():
            file_path, file_name, file_path = self.upload_resource_file(storage)
            if not file_path:
                return make_response((
                    json.dumps({"status": 10001, "msg": "文件类型不正确"}),
                    200,
                    {'Content-Type': 'application/json; charset=utf-8'}
                ))
            return make_response((
                json.dumps({"status": 10000, "file_name": file_name, "file_path": file_path}),
                200,
                {'Content-Type': 'application/json; charset=utf-8'}
            ))

    def index(self):
        """
        :return:
        """
        user_type = session['user_type']
        return render_template('open_file.html', user_type=user_type)
