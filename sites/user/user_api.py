#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime
from sites import db

from flask import request, make_response, render_template, redirect, session
from sites.user.model import User


class UserService(object):
    """
    api
    """

    def login(self):
        """
        登录
        :return:
        """
        # 获取用户名和密码
        user_name = request.json.get('user_name')
        pass_word = request.json.get('pass_word')
        # 查询验证
        record = User.query.filter(User.user_name == user_name, User.pass_word == pass_word).first()
        if not record:
            return make_response({"status": 10001, "msg": "账号/密码错误"})
        session['user'] = user_name
        session['user_id'] = record.id
        session['user_type'] = record.user_type
        return make_response({"status": 10000, "msg": "成功", "user_type": record.user_type})

    def logout(self):
        del session['user']
        del session['user_type']
        return redirect('/')

    def list(self):
        """
        列表
        :return:
        """
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        # 查询条件参数
        user_name = request.args.get('user_name', '')
        args = [User.user_type != 1]
        if user_name:
            args.append(User.user_name.like('%{}%'.format(user_name)))
        records = User.query.filter(*args)
        total = records.count()
        result = []
        for record in records[(page - 1) * limit:page * limit]:
            user_type = "教师" if record.user_type == 2 else "学生"
            result.append({
                "id": str(record.id),
                "user_name": record.user_name,
                "pass_word": '********',
                "user_type": user_type,
                "update_time": record.update_time,
                "create_time": record.create_time,
            })
        return make_response({"code": 0, "data": result, "count": total})

    def add(self):
        user_name = request.args.get('user_name')
        pass_word = request.args.get('pass_word')
        user_type = request.args.get('user_type')
        if User.query.filter(User.user_name == user_name).first():
            return make_response((
                json.dumps({"status": 10001, "msg": "用户名已存在"}),
                200,
                {'Content-Type': 'application/json; charset=utf-8'}
            ))
        if not all([user_name,pass_word]):
            return make_response((
                json.dumps({"status": 10001, "msg": "用户名密码必填"}),
                200,
                {'Content-Type': 'application/json; charset=utf-8'}
            ))
        record = User()
        record.user_name = user_name
        record.pass_word = pass_word
        record.user_type = user_type
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
        user_name = request.args.get('user_name')
        pass_word = request.args.get('pass_word')
        user_type = request.args.get('user_type')
        _id = request.args.get('id')
        record = User.query.filter(User.id == _id).first()
        record.user_name = user_name
        record.pass_word = pass_word
        record.user_type = user_type
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
        User.query.filter(User.id == _id).delete()
        db.session.commit()
        return make_response((
            json.dumps({"status": 10000, "msg": "成功"}),
            200,
            {'Content-Type': 'application/json; charset=utf-8'}
        ))

    def get(self):
        _id = request.args.get('id')
        record = User.query.filter(User.id == _id).first()
        result = {
            "id": record.id,
            "user_name": record.user_name,
            "pass_word": record.pass_word,
            "user_type": str(record.user_type)
        }
        return make_response({"code": 0, "data": result})

    def dispatch(self, func):
        """
        函数调度
        """
        map_func = {
            "login": self.login,
            "logout": self.logout,
            "list": self.list,
            "add": self.add,
            "get": self.get,
            "edit": self.edit,
            "delete": self.delete,
            "user_edit_page": self.user_edit_page,
            "user_page": self.user_page,
        }
        if func in map_func:
            return map_func[func]()

    def user_edit_page(self):
        _id = request.args.get('id')
        return render_template('user_add.html', id=_id)

    def user_page(self):
        _id = request.args.get('id')
        return render_template('user.html', id=_id)

