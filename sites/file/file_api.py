#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime
import time

from sites import db

from flask import request, make_response, render_template, redirect, session, send_file
from sites.file.model import File


class FileService(object):
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
        file_type = int(request.args.get('type'))
        if file_type == 1:
            type_list = ['doc', 'docx']
        elif file_type == 2:
            type_list = ['xls', 'xlsx', 'csv']
        else:
            type_list = ['bmp', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd',
                         'dxf', 'ufo', 'jpeg',
                         'eps', 'ai', 'raw', 'WMF', 'webp', 'avif', 'apng']

        records = File.query.filter(File.private == 1, File.operator == session['user'], File.file_type.in_(type_list))
        total = records.count()
        result = []
        for record in records[(page - 1) * limit:page * limit]:
            result.append({
                "id": str(record.id),
                "file_name": record.file_name,
                "operator": record.operator,
                "update_time": record.update_time,
                "create_time": record.create_time,
            })
        return make_response({"code": 0, "data": result, "count": total})

    def add(self):
        file_path = request.args.get('file_path')
        file_name = request.args.get('file_name')
        record = File()
        record.file_path = file_path
        record.file_name = file_name
        record.file_type = file_name.split('.')[-1]
        operator = session['user']
        record.operator = operator
        record.private = 1
        record.private_file_path = ''
        record.can_view_operator = ''
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
        file_path = request.args.get('file_path')
        file_name = request.args.get('file_name')
        _id = request.args.get('id')
        record = File.query.filter(File.id == _id).first()
        record.file_path = file_path
        record.file_name = file_name
        record.file_type = file_name.split('.')[-1]
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
        return make_response(
            send_file(os.path.join(os.path.abspath('templates'), 'layui', "temp", record.file_path),
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
            "add_page": self.add_page,
            "edit_page": self.edit_page,
            "down": self.down,
            "word_edit_page": self.word_edit_page,
            "picture_edit_page": self.picture_edit_page
        }
        if func in map_func:
            return map_func[func]()
    def add_page(self):
        _id = request.args.get('id')
        file_type = int(request.args.get('type'))
        return render_template('file_edit.html', id=_id, file_type=file_type)
    def edit_page(self):
        _id = request.args.get('id')
        file_type = int(request.args.get('type'))
        return render_template('database.html', id=_id, file_type=file_type)
    def word_edit_page(self):
        _id = request.args.get('id')
        file_type = int(request.args.get('type'))
        return render_template('word.html', id=_id, file_type=file_type)
    def picture_edit_page(self):
        _id = request.args.get('id')
        file_type = int(request.args.get('type'))
        return render_template('picture.html', id=_id, file_type=file_type)
    def upload_resource_file(self, storage):
        """
        上传文件并且保存
        :param storage:
        :return:
        """
        file_type = int(request.args.get('type'))
        if file_type == 1:
            type_list = ['doc', 'docx']
        elif file_type == 2:
            type_list = ['xls', 'xlsx', 'csv']
        else:
            type_list = ['bmp', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd',
                         'dxf', 'ufo', 'jpeg',
                         'eps', 'ai', 'raw', 'WMF', 'webp', 'avif', 'apng']
        file_data = storage.read()
        file_path = str(int(time.time())) + storage.filename
        if storage.filename.split('.')[-1] not in type_list:
            return 0, 0, 0

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
        file_type = int(request.args.get('type'))
        if(file_type==2):
          return render_template('file.html', file_type=file_type)
        if(file_type==1):
            return render_template('file_word.html', file_type=file_type)
        if(file_type==3):
            return render_template('file_picture.html', file_type=file_type)