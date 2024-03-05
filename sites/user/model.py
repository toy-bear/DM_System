#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sites import db, app

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = db.Column(db.String(32), nullable=False)
    pass_word = db.Column(db.String(32), nullable=False)
    # 1 管理员 2 教师 3 学生
    user_type = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(255), nullable=False)
    update_time = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()

